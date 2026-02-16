from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

@tool
def triple_number(number: int) -> int:
    """
    Apply redis' propertiery triplet logic to the given number.
    
    Args:
        number: The number to be tripled
        
    Returns:
        The tripled number
    """
    return number * 3


tools = [TavilySearch(max_results=1), triple_number]

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0).bind_tools(tools)