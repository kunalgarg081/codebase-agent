import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from app.llm import ask_llm
from app.prompts import SYSTEM_PROMPT
from app.tool_executor import execute

console = Console()

MAX_TOOL_CALLS = 5
MAX_HISTORY = 20
WRITE_TOOLS = {
    "write_file",
}
DEBUG = True

class Agent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def _trim_history(self):
        """
        Keep the system prompt and only
        the most recent conversation.
        """

        if len(self.messages) <= MAX_HISTORY:
            return

        system = self.messages[0]

        recent = self.messages[-MAX_HISTORY:]

        self.messages = [
            system,
            *recent,
        ]

    def _confirm_write(self, path: str) -> bool:
        """
        Ask the user before modifying a file.
        """
    
        console.print()
    
        console.print(
            Panel(
                f"[bold yellow]Tool[/bold yellow] : write_file\n"
                f"[bold yellow]File[/bold yellow] : {path}",
                title="[bold red]⚠ File Modification[/bold red]",
                border_style="red",
            )
        )
    
        console.print()
    
        return Confirm.ask(
            "[bold cyan]Approve this operation?[/bold cyan]"
        )
    def chat(self, user_message: str) -> str:
        """
        Process a user message using a multi-step
        tool-calling loop.
        """

        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        for step in range(MAX_TOOL_CALLS):

            reply = ask_llm(self.messages)

            if DEBUG:
                print("\n========== RAW MODEL RESPONSE ==========")
                print(reply)
                print("========================================\n")

            # Final response
            if not reply.tool_calls:

                self.messages.append(reply)

                self._trim_history()

                return reply.content

            # Save assistant message
            self.messages.append(reply)

            # Execute requested tools
            for tool_call in reply.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                # Ask before modifying files
                if tool_name in WRITE_TOOLS:

                    if not self._confirm_write(
                        arguments.get("path", "")
                    ):
                        return "Operation cancelled by user."

                result = execute(
                    tool_name,
                    arguments,
                )

                if DEBUG:
                    print(
                        f"Executed: {tool_name}({arguments})"
                    )

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    }
                )

        self._trim_history()

        return (
            "Maximum tool call limit reached. "
            "Unable to complete the request."
        )
