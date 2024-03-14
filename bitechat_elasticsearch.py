from langchain.tools import BaseTool
import googlemaps
from elasticsearch import Elasticsearch
from langsmith import Client
from langchain.callbacks import LangChainTracer
import os
from typing import List, Dict, Optional, Type
from sentence_transformers import SentenceTransformer
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import json

load_dotenv()

## Coordinate Search Tool
class CoordinateSearchTool(BaseTool):
    name = "Coordinate_Search"
    description = """Use this tool to search for the coordinates of a location.
    """

    def _run(self, location: str):
        """
        Search for the coordinates of a location.

        Args:
            location (str): The location to search for.

        Returns:
            tuple: A tuple containing the latitude and longitude of the location.
        """
        gmpas = googlemaps.Client(key=os.getenv('GOOGLE_API'))
        print(location)
        geocode_result = gmpas.geocode(location)
        if geocode_result:
            print(geocode_result[0]['geometry']['location'])
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']  
            return lat, lng
        else:
            print('No place result found')
            lat = None
            lng = None
            return lat, lng
        
    def _arun(location: str):
        raise NotImplementedError("This tool does not support async")
    

## Elasticsearch query tool
class ElasticSearchToolSchema(BaseModel):
    query: str = Field(..., description="The query string to search for")
    lat: Optional[float] = Field(None, description="Latitude for geo-location based search")
    lon: Optional[float] = Field(None, description="Longitude for geo-location based search")
    pass

class ElasticSearchTool(BaseTool):
    args_schema: Type[BaseModel]=ElasticSearchToolSchema
    name = "Elasticsearch_Query_Tool"
    description = """
    Use this tool to query Elasticsearch for restaurant information. Input a dictionary with query, lat (optional), lon(optional).
    """
    
    def _run(self, **kwargs: str) -> List[Dict]:
        # make sure cloud_id is formatted correctly
        cloud_id = os.getenv('ELASTICSEARCH_ID')
        if not cloud_id.endswith("=="):
            cloud_id += "=="
        print(cloud_id)

        es = Elasticsearch(
            cloud_id=cloud_id,
            basic_auth=("elastic", os.getenv('ELASTICSEARCH_PWD'))
        )

        # Default values
        query = kwargs.get('query', '')
        lat = kwargs.get('lat', None)
        lon = kwargs.get('lon', None)
        index = 'bitechat'
        
        print(f"Index: {index}, Query: {query}, Latitude: {lat}, Longitude: {lon}")

        # Construct the geo_distance filter if lat and lon are provided
        geo_distance_filter = {}
        if lat is not None and lon is not None:
            geo_distance_filter = {
                "filter": [{
                    "geo_distance": {
                        "distance": "2km",
                        "location": {"lat": lat, "lon": lon}
                    }
                }]
            }

        # Create embedding vector for the query
        model = SentenceTransformer('intfloat/e5-small-v2')
        vector = model.encode(query, normalize_embeddings=True).tolist()
        print("Vector created.")

        # Hybrid search
        response = es.search(
            index=index,
            size=3,
            query={
                "bool": {
                    "must": {
                        "match_all": {}
                    }
                }
            },
            _source=["info", "food", "review_summary"],
            knn={
                "field": "review_vector",
                "query_vector": vector,
                "k": 5,
                "num_candidates": 15,
                **geo_distance_filter
            },
            rank={"rrf": {}},
        )

        results = []
        for hit in response['hits']['hits']:
            source = hit['_source']
            formatted_source = {
                'info': source.get('info', 'No information available'),
                'popular_dishes': source.get('food', 'Popular dishes not available'),
                'review_summary': source.get('review_summary', 'Review summary not available')
        }
            results.append(formatted_source)

        return results

    def _arun(self, **kwargs: str) -> List[Dict]:
        raise NotImplementedError("This tool does not support async")

## Chat Agent Manager
class AgentManger:
    def __init__(self, config_path='config.json'):

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # LangSmith Configurations
        self.callbacks = [
            LangChainTracer(
                project_name=os.getenv('LANGCHAIN_PROJECT'),
                client=Client(
                api_url="https://api.smith.langchain.com",
                api_key=os.getenv('LANGCHAIN_API_KEY')
                )
            )
            ]

        self.llm = ChatOpenAI(
            api_key=os.getenv('OPENAI_API_KEY'), 
            temperature=self.config.get('chat_temperature'),
            model_name=self.config.get('chat_model'),
        )
        self.tools = [CoordinateSearchTool(), ElasticSearchTool()]
        self.chat_agent = self.create_agent(instruction=self.config.get('chat_instruction'))
        # self.agent_executor = AgentExecutor(agent=self.chat_agent, tools=self.tools, verbose=True)

    def create_agent(self, instruction):
        """
        Create an agent that uses the OpenAI language model and the specified tools.

        Args:
            llm (ChatOpenAI): The language model to use.
            tools (List[BaseTool]): The tools to use.
            prompt (ChatPromptTemplate): The prompt to use.

        Returns:
            Agent: The created agent.
        """
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(instruction),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate.from_template("{input}"), 
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        print(prompt)

        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        # add history to the agent
        message_history = ChatMessageHistory()
        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: message_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        return agent_with_chat_history

    def chat_with_agent(self, input_message, session_id):
        """
        """
        result = self.chat_agent.invoke(
            {"input": input_message},
            config={"configurable": {"session_id": session_id}, "callbacks": self.callbacks}
        )

        return result

## Initialize the agent manager  
rag_agent = AgentManger()

## Create a chat function for application to use
def chat(user_message, session_id):
    return rag_agent.chat_with_agent(user_message, session_id)
