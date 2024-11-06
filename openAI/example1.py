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


def main ():
    print("showtime now !!!")

    OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    

    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=get_api_key("OPENAI_API_KEY"),
    )

    ## model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

    prompt = "Tell me about the capital of France."

    response = client.chat.completions.create(
           model="gpt-4-turbo",  
           messages=[
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": prompt}
           ]
       )
    #response.choices[0].message['content']
    response_message = response.choices[0].message.content

    ## response = get_gpt4_response(user_prompt)
    print(response_message)
   
if __name__ == "__main__":
    main()
