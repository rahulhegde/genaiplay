# weather 

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather_mcp")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # For demonstration purposes, we'll return a mock weather report.
    return f"The current weather in {city} is sunny with a temperature of 25°C."

if __name__ == "__main__":
    mcp.run(transport="sse")