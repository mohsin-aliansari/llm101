## Simple example of embeddings using langchain.

import configparser
from langchain.embeddings import OpenAIEmbeddings

def get_api_key(source: str):
    config = configparser.ConfigParser()
    config.read('..\\config.ini')
    api_key = config.get('KEYS',source)
    return api_key
  
def main():
    print("This is the simple example of embeddings using langchain")
    
    OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")
    # Initialize the embeddings model
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    print (embeddings)
    
    # Text to embed
    text = "OpenAI"
    
    # Create the embedding
    embedding = embeddings.embed_query(text)

    file = open("output2.txt", "w")
    print(embedding, file=file)
    file.close()
if __name__ == "__main__":
    main()