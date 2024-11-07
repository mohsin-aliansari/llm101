import os
import configparser

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


def get_api_key(source: str):
    config = configparser.ConfigParser()
    config.read('..\\config.ini')
    api_key = config.get('KEYS',source)
    return api_key

## Read the document
def read_doc(directory):
    file_loader=PyPDFDirectoryLoader(directory)
    documents=file_loader.load()
    return documents

## Divide the docs into chunks
### https://api.python.langchain.com/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html#
def chunk_data(docs,chunk_size=800,chunk_overlap=50):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    doc=text_splitter.split_documents(docs)
    return docs


def main():
    print("lets begin the fun :-)")
    
    PINECONE_API_KEY = get_api_key("PINECONE_API_KEY")
    OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")

    os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

    doc=read_doc('documents/')
    len(doc)
    documents=chunk_data(docs=doc)
    len(documents)
    
    embeddings=OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    
    index_name = "myvectorindex"

    # Connect to Pinecone index and insert the chunked docs as contents
    #index = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)


    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("myvectorindex")
    
    vectorstore = PineconeVectorStore(index, embeddings)

    # query = "who are the passegers in itineray"
    #docs = vectorstore.similarity_search(query,k=3)
    #print(docs[0].page_content)
    #print(docs)

    template = """
    Answer the question based on the context below. If you can't 
    answer the question, reply "I don't know".

    Context: {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    parser = StrOutputParser()

    #retriever = vectorstore.as_retriever()

    chain = (
        {"context": vectorstore.as_retriever(), "question": RunnablePassthrough()}
        | prompt
        | model
        | parser
    )
    response = chain.invoke("how is the weather today")
    #response = chain.invoke("what is my wife name")
    # response = chain.invoke("tell me the travelers in the flight itineray")
    print(response)
if __name__ == "__main__":
    main()
