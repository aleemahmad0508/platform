from mcp_instance import mcp

print("importing tools .....")
import tools
print("tools are imported successfully...")
if __name__ == "__main__":
    print("Starting Kubernetes MCP Server...")
    mcp.run(transport="streamable-http")