from dataclasses import dataclass


@dataclass
class AgentState:
    """
    Runtime state of the agent during a conversation.
    """

    tool_calls: int = 0
    last_tool: str | None = None
    last_error: str | None = None
    steps: int = 0

    def reset(self):
        self.tool_calls = 0
        self.last_tool = None
        self.last_error = None
        self.steps = 0
