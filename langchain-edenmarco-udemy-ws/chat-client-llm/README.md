## coverage
Following items were covered (langchain 1.0.0 alpha)
- chat clients with any LLM - close (hosted on Groq) or open source (installed using ollama)
- use of langsmith for tracing, configured through .env

## setting up workspace
uv venv
uv init
uv add langchain-core langchain-openai langchain-groq langchain-ollama dotenv

## running model locally
ollama pull deepseek-r1:1.5b
ollama run deepseek-r1:1.5b