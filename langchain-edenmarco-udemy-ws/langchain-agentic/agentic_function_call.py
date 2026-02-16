"""
LangChain agent with GROQ and Tavily search using function calling.
"""

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient


# Load environment variables
load_dotenv()


@tool
def tavily_search(query: str) -> str:
    """
    Search the web using Tavily search API.
    
    Args:
        query: The search query to execute
        
    Returns:
        A string containing the search results
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        return "Error: TAVILY_API_KEY not found in environment variables"
    
    try:
        client = TavilyClient(api_key=tavily_api_key)
        response = client.search(query=query, search_depth="advanced", max_results=5)
        
        # Format the results
        results = []
        if response.get("results"):
            for result in response["results"]:
                title = result.get("title", "No title")
                url = result.get("url", "No URL")
                content = result.get("content", "No content")
                results.append(f"Title: {title}\nURL: {url}\nContent: {content}\n")
        
        return "\n---\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Error performing search: {str(e)}"


def main():
    """
    Main function to run the LangChain agent with GROQ and Tavily search.
    """
    # Get API keys from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("Error: GROQ_API_KEY not found in environment variables")
        print("Please set GROQ_API_KEY in your .env file or environment")
        return
    
    # Initialize the GROQ chat model
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=groq_api_key,
        temperature=0.1
    )
    
    # Bind the Tavily search tool to the LLM
    llm_with_tools = llm.bind_tools([tavily_search])
    
    print("LangChain Agent with GROQ and Tavily Search")
    print("=" * 50)
    print("Type 'quit' or 'exit' to end the conversation\n")
    
    # Conversation loop
    conversation_history = []
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        conversation_history.append(HumanMessage(content=user_input))
        
        # Get response from LLM
        response = llm_with_tools.invoke(conversation_history)
        
        # Add AI response to history
        conversation_history.append(response)
        
        # Check if the LLM wants to call a tool
        if response.tool_calls:
            print(f"\nAssistant: {response.tool_calls}")
            print("\n[Agent is searching the web...]")
            
            # Execute tool calls
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                if tool_name == "tavily_search":
                    search_query = tool_args.get("query", "")
                    search_results = tavily_search.invoke({"query": search_query})
                    print(f"\ntool search response: {search_results}\n")

                    # Add tool result to conversation using ToolMessage
                    tool_message = ToolMessage(
                        content=search_results,
                        tool_call_id=tool_call["id"],
                    )
                    conversation_history.append(tool_message)
            
            # Get final response with tool results
            final_response = llm_with_tools.invoke(conversation_history)
            conversation_history.append(final_response)
            print(f"\nAssistant: {final_response.content}\n")
        else:
            print(f"\nAssistant: {response.content}\n")


if __name__ == "__main__":
    main()
