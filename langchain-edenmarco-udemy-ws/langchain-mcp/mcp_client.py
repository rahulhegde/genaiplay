import asyncio
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()



llm = ChatGroq(model="openai/gpt-oss-20b")

async def main():
    print("Hello from langchain-mcp client stdio!")

    client = MultiServerMCPClient(
        {
            "math_mcp": {
                "command": "python3",
                "args": ["/home/developer/workspace/python-ws/langchain-edenmarco-udemy-ws/langchain-mcp/mcp-server/math_mcp.py"],
                "transport": "stdio",
            },"weather_mcp": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    )

    tools = await client.get_tools()
    print (f"Available tools: {tools}\n")

    agent = create_agent(model=llm, tools=tools)

    # ainvoke the agent - async call
    result = await agent.ainvoke({"messages": [{"role": "user", "content": "use the tools to solve 2 problems. (1) what is 2+2*3 ? (2) what is weather in India?"}]})
    print (f"Agent Result: {result}\n")

if __name__ == "__main__":
    asyncio.run(main())