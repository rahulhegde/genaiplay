uv venv
. .venv/bin/activate

## refer to the dependenccy list
uv add langchain-core langchain-openai langchain-groq langchain-ollama dotenv

    "black>=26.1.0",
    "fastmcp>=2.14.3",
    "isort>=7.0.0",
    "langchain>=1.2.6",
    "langchain-core>=1.2.7",
    "langchain-groq>=1.1.1",
    "langchain-mcp-adapters>=0.2.1",
    "python-dotenv>=1.2.1",

## background of this task
- MCP server list down two types of servers 
 - math_mcp_server - uses stdio (interprocess communication) 
 - weather_mcp_server - which runs HTTP server, communication using Server sent event (SSE)

 - mcp_client - is the host which also encapsulates the mcp client that creates multi-client session with 
 with mcp servers (2 in this case)

 - simple question in the prompt, calls the required tools multiple times using mcp protocol.

## run

-- run the mcp server on localhost:8000 (default) as it uses SSE
cd uv run weather_mcp.py;
uv run weather_mcp.py

-- no need to run math mcp server as it uses stdio and will be launched internally by client host

-- run the mcp client
cd langchain-mcp;
uv run mcp_client.py
