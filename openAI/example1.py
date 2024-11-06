import os
import configparser
from openai import OpenAI
import openai

##from langchain_openai.chat_models import ChatOpenAI
##from langchain_core.output_parsers import StrOutputParser

##from langchain.prompts import ChatPromptTemplate
##from operator import itemgetter


def get_api_key(source: str):
    config = configparser.ConfigParser()
    config.read('..\\config.ini')
    api_key = config.get('KEYS',source)
    return api_key

def ask_model(prompt):
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=get_api_key("OPENAI_API_KEY"),
    )

    ## model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

    #prompt = "Tell me something about pakistan"

    response = client.chat.completions.create(
           model="gpt-4-turbo",  
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": prompt}
           ]
       )
    #response.choices[0].message['content']
    response_message = response.choices[0].message.content

    return response_message

def main ():
    print("showtime begins !!!")

    # OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")
    # os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    
    while True: # prompt != "end":
        prompt = input("How can I help you?") 
        if prompt != 'end':
            response = ask_model(prompt)
            ## response = get_gpt4_response(user_prompt)
            print(response)
        else:
            print ("bye bye")
   
if __name__ == "__main__":
    main()
