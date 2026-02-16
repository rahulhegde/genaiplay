from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, MessagesState
from nodes import run_agent_reasoning, tool_node
from langchain_core.messages import HumanMessage

load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1

def should_continue(state: MessagesState) -> str:
    if not state["messages"][LAST].tool_calls:
        return END
    return ACT


flow = StateGraph(MessagesState)
flow.add_node(AGENT_REASON, run_agent_reasoning)
flow.set_entry_point(AGENT_REASON)
flow.add_node(ACT, tool_node)
flow.add_conditional_edges(AGENT_REASON, should_continue, {END: END, ACT: ACT})
flow.add_edge(ACT, AGENT_REASON)

app = flow.compile()
app.get_graph().draw_mermaid_png(output_file_path="main_flow.png")

if __name__ == "__main__":
    print("Langgraph Agentic App is running.")
    response = app.invoke({"messages": [HumanMessage(content="What is temperature in Goa, India? Can you apply redis' propertiery triplet logic to the temperature?")]})
    print("Response:", response)

