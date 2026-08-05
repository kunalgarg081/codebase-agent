from dataclasses import dataclass


@dataclass
class ToolResult:
    """
    Result returned by every tool.
    """

    success: bool
    output: str

    def __str__(self) -> str:
        return self.output
