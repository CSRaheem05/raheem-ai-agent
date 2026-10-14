from datetime import datetime
from mcp.server import MCPServer

mcp = MCPServer("University Tools")


@mcp.tool()
def current_date() -> str:
    """Get today's current date."""
    return datetime.now().strftime("%Y-%m-%d")


@mcp.tool()
def get_university_name() -> str:
    """Get the name of the university."""
    return "Zarqa University"


@mcp.tool()
def get_student_count() -> str:
    """Get the total number of students at the university."""
    return "5000"


if __name__ == "__main__":
    mcp.run()
