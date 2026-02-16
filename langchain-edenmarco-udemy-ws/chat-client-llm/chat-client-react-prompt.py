from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import os
import getpass

load_dotenv()

def main():
    print("Hello from langchain-edenmarco-udemy-ws!")
    print (os.getenv("OPENAI_API_KEY"))

    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

    user_data = '''
    LangChain is a framework for developing applications powered by language models.
    It enables developers to build applications that can interact with various data sources,
    perform complex reasoning, and manage conversational contexts effectively.
    '''

    user_template = '''
    Summarize the following {information} in a concise manner.
    1. short summary in single line
    2. one Interesting insight
    '''

    # create a prompt template 
    prompt_template = PromptTemplate(
        input_variables=["information"],
        template=user_template,
    )

    #llm = ChatOpenAI(model="gpt-4o")
    #llm = ChatGroq(model="openai/gpt-oss-20b")

    ### use ollama (client) to download the model on the your system, llama3:latest in this case
    #llm = ChatOllama(model="llama3:latest")
    llm = ChatOllama(model="deepseek-r1:1.5b")

    # option1 - direct invocation
    #prompt = prompt_template.format(text=information)
    #result = llm.invoke(prompt)

    # option2 - chaining
    chain = prompt_template | llm
    result = chain.invoke(input = {"information": user_data})

    print(result.content)

if __name__ == "__main__":
    main()
