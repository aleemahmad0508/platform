from mcp.server.fastmcp import FastMCP

print("Creating FastMCP instance")

mcp = FastMCP(
    "devops-mcp",
    host="0.0.0.0",
    port=8000,
)

print("FastMCP created")