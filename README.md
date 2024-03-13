# BiteChat
An AI food discovery specialist

![bitechat](https://github.com/phwamy/bitechat/blob/main/img/bitechat_logo.png?raw=true)

## Problem - Dining Discovery is Broken
Deciding where to eat shouldn't be a chore, especially when you have dietary restrictions or specific cravings. Scouring reviews and filtering results shouldn't take away from the joy of a good meal.

![problem](https://github.com/phwamy/bitechat/blob/main/img/problem.png?raw=true)

## What We Offer
Our smart technology gets you from craving to dining table in record time. Get instant, tailored recommendations that leave you satisfied – not stressed.

* Smart spending, savory meals
* Dining experiences elavated
* Save your invaluabe time
* Hidden gems unveiled

![solution](https://github.com/phwamy/bitechat/blob/main/img/solution.png?raw=true)

## Key Features
* **Hyper-personalized restaurant recommendations:** Get spot-on suggestions based on your cravings, dietary needs, and favorite flavors.
* **Dish-driven restaurant discovery:** Search by your dream dish and find the restaurants that make it best.
* **Signature dish and taste-matched ordering:** Uncover must-try dishes and avoid menu misses with recommendations tailored to your preferences.

## Demo Site
[BiteChat](https://bitechat.streamlit.app/)

## Technology
We've developed a Retrieval Augmented Generation (RAG) chatbot built on Elasticsearch. This solution leverages Elasticsearch's hybrid search capabilities (combining full-text and vector search) to accurately retrieve information from diverse data sources, enhancing precision compared to semantic search alone. Our approach integrates the contextual understanding of Large Language Models (LLMs) with Elasticsearch's robust search functionality, delivering personalized restaurant and meal suggestions while minimizing inaccurate responses.

We employ a Langchain agent powered by an LLM to interpret user intent and execute tasks. These tasks include customizing functions like geocoding and using the Elasticsearch tool to gather restaurant data, synthesize information, and generate tailored responses.

* Data source: Google Maps
* Models: 
    * Popular dishes extraction: (Mistral v0.2)[https://ollama.com/library/mistral] model
    * Reivew summarization: (facebook/bart-large-cnn)[https://huggingface.co/facebook/bart-large-cnn] model
    * Embeddings: (intfloat/e5-small-v2)[https://huggingface.co/intfloat/e5-small-v2] model
    * Chat: (gpt-3.5-turbo-0125)[https://platform.openai.com/docs/models/gpt-3-5-turbo] model
* Search Engine: Elastic Cloud
* Agent and Tools: Use `langchain` to create an agent that controls geocoding tool and Elasticsearch retrieval tool. 
* Deployment: Streamlit Community Cloud

## Meet the Team
* Business Plan: Anushuka Soni & Jasper Huang
* Market Research: Hannah Tsao
* User Experience Research: Shivam Mittal
* Project Manager: Zach Anderson
* Machine Learning Engineer: [PeiHsin Wang](phw.amy@gmail.com)

