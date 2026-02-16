from dotenv import load_dotenv
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode

from react import llm, tools

# Load environment variables
load_dotenv()

SYSTEM_MESSAGE = """You are an intelligent agent designed to assist users by leveraging various tools."""

def run_agent_reasoning(state: MessagesState) -> MessagesState:
    """
    Run the agent reasoning mode.

    """

    response = llm.invoke([{"role": "system", "content": SYSTEM_MESSAGE}, *state["messages"]])

    return {"messages": [response]}

tool_node = ToolNode(tools)