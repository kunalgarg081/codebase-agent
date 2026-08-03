from app.tools import TOOLS


def execute(tool_name, arguments):

    tool = TOOLS.get(tool_name)

    if tool is None:
        return f"Unknown tool '{tool_name}'."

    return tool(**arguments)