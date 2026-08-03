from app.tools import TOOLS


def execute(tool_name: str, arguments: dict):
    """
    Execute a registered tool with the given arguments.
    """

    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown tool: {tool_name}"

    try:
        return tool(**arguments)

    except TypeError as e:
        return (
            f"Invalid arguments for tool '{tool_name}': {e}"
        )

    except Exception as e:
        return (
            f"Error while executing '{tool_name}': {e}"
        )