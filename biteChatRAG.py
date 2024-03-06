###
# This is a command line interface for the BiteChat assistant.
# Type `python biteChatRAG.py -i "your-message"` to start your food discovery journey.
###


import argparse
from pprint import pprint
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
file_id = os.getenv('FILE_ID')
assistant_id = os.getenv('ASSISTANT_ID')

client=OpenAI(api_key = api_key)

class BiteChaAssistant:
    def __init__(self, client, assistant_id, thread_id_file='thread_id.txt'):
        self.client = client
        self.assistant_id = assistant_id
        self.thread_id_file = thread_id_file
        self.thread_id = self.get_or_initiate_thread()  

    def get_or_initiate_thread(self):
        ### For command lin test use, no need for web application
        # Try to read an existing thread_id from the file
        try:
            with open(self.thread_id_file, 'r') as file:
                thread_id = file.read().strip()
            if thread_id:
                print(f"Using existing thread ID: {thread_id}")
                return thread_id
        except FileNotFoundError:
            pass  

        # No valid thread_id found; initiate a new thread
        thread = self.client.beta.threads.create()
        thread_id = thread.id
        with open(self.thread_id_file, 'w') as file:
            file.write(thread_id)
        print(f"New thread initiated with ID: {thread_id}")
        ###

        return thread.id

    def run_bitechat(self, user_message):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role='user',
            content=user_message
        )
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id,
            instructions="Please address the user as Husky. Be attentive and passionate."
        )

        run_status = ""
        while run_status not in ["completed", "failed"]:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )
            run_status = run.status
            print(run_status)
            time.sleep(8)

        if run_status == "completed":
            time.sleep(2)
            messages = self.client.beta.threads.messages.list(thread_id=self.thread_id)
            messages_list = [each.content[0].text.value for each in messages]
            response = messages_list[0]
            print(response)
            return response
        else:
            response = "The exercise did not complete successfully."
            print(response)
            return response
            
        
def main():
    assistant = BiteChaAssistant(client, assistant_id)

    parser = argparse.ArgumentParser(description='Command Line Assistant')
    parser.add_argument('-i', '--input', type=str, required=True, help='User message to send to the assistant')
    args = parser.parse_args()

    assistant.run_bitechat(args.input)

if __name__ == "__main__":
    main()

