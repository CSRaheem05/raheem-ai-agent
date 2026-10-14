from mcp import Client, StdioServerParameters


def get_server():
    return StdioServerParameters(command="python", args=["mcp_server/server.py"])


async def list_mcp_tools():
    server = get_server()

    async with Client(server) as client:
        tools = await client.list_tools()

        return [
            {"name": tool.name, "description": tool.description} for tool in tools.tools
        ]


async def call_mcp_tool(tool_name: str, arguments: dict = None):
    server = get_server()

    async with Client(server) as client:
        result = await client.call_tool(tool_name, arguments or {})

        return result.structured_content["result"]
