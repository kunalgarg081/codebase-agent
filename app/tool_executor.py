from app.tools import TOOLS
from app.tool_result import ToolResult

def execute(tool_name: str, arguments: dict):
    """
    Execute a registered tool with the given arguments.
    """

    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    function = tool["function"]

    try:
        return ToolResult(
            success=True,
            output=str(function(**arguments)),
        )

    except TypeError as e:
        return ToolResult(
            success=False,
            output=(
                f"Invalid arguments for tool "
                f"'{tool_name}': {e}"
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            output=(
                f"Error while executing '{tool_name}': {e}"
            ),
        )