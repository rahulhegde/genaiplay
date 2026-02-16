# refer README.md for context

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

# Load environment variables
load_dotenv()

@tool
def get_string_length(input_string: str) -> int:
    """
    Get the length of a given string.
    
    Args:
        input_string: The string to measure
        
    Returns:
        The length of the string as an integer
    """
    print(f"length of the string - : {input_string}")

    return len(input_string)

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
tools = [TavilySearch(), get_string_length]
agent = create_agent(model=llm, tools=tools)


def main():
    print("LangChain Agentic Agent with GROQ and Tavily")
    print("=" * 50)
    while True:
        user_query = input("Human: ")
        if user_query.lower() == "quit" or user_query.lower() == "exit":
            break
        response = agent.invoke({"messages": HumanMessage(content=user_query)}) 
        print("\n[Agent has completed the task]")
        print(f"Agent Response: {response}")

if __name__ == "__main__":
    main()
