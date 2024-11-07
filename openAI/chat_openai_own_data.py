import os
import openai
import configparser
import PyPDF2

chat_model = "gpt-3.5-turbo"

def get_api_key(source: str):
    config = configparser.ConfigParser()
    config.read('..\\config.ini')
    api_key = config.get('KEYS',source)
    return api_key

def ask_model(context: str, chat_model: str):
    result = openai.chat.completions.create(model=chat_model, messages=context)
    return result.choices[0].message.content

def extract_pdf(file_name: str) -> str:
    pdf_text =""

    # creating a pdf file object
    pdf_file_obj = open(file_name, 'rb')

    # creating a pdf reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    
    # printing number of pages in pdf file
    #print(len(pdf_reader.pages))
    
    # creating a page object
    page_obj = pdf_reader.pages[0]

    # extracting text from page
    pdf_text = page_obj.extract_text()
    # print(pdf_text)
    
    # closing the pdf file object
    pdf_file_obj.close()
    print(pdf_file_obj)

    return pdf_text

def get_messages(context_str: str, question: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": """
You will receive a question from the user and some context to help you answer the question.

Evaluate the context and provide an answer if you can confidently answer the question.

If you are unable to provide a confident response, kindly state that it is the case and explain the reason.

Prioritize offering an "I don't know" response over conveying potentially false information.

The user will only see your response and not the context you've been provided. Thus, respond in precise detail, directly repeating the information that you're referencing from the context.
""".strip(),
        },
        {
            "role": "user",
            "content": f"""
Using the following information as context, I'd like you to answer a question.

{context_str}

Please answer the following question: {question}
""".strip(),
        },
    ]

def main():
    openai.api_key = get_api_key("OPENAI_API_KEY")
    
    pdf_text = extract_pdf("receipts.pdf")
    
    while True: # prompt != "end":
        prompt = input("Enter question pls.")
        if prompt != 'end':
            messages = get_messages(pdf_text, prompt)   
            response = ask_model(messages,chat_model)
            print(response)
        else:
            print ("Good bye !!!")
            break
   
if __name__ == "__main__":
    main()

