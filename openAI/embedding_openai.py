import os
import configparser
import openai

def get_api_key(source: str):
    config = configparser.ConfigParser()
    config.read('..\\config.ini')
    api_key = config.get('KEYS',source)
    return api_key
    
def get_embedding(text, model="text-embedding-ada-002"):
    # replace newlines, which can negatively affect performance.
    text = text.replace("\n", " ")
    return openai.embeddings.create(input=text, model=model).data[0].embedding


def main():
    print("Let the show begin !!!!")
    openai.api_key= get_api_key("OPENAI_API_KEY")
    model="text-embedding-ada-002"
    text = "OpenAI"
    embeddings = get_embedding(text, model)
    print(len(embeddings))
    print (embeddings)
    
    file = open("output.txt", "w")
    print(embeddings, file=file)
    file.close()
if __name__ == "__main__":
    main()