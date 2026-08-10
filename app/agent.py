from email.mime import message
import json
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from app.llm import ask_llm
from app.prompts import SYSTEM_PROMPT
from app.tool_executor import execute
from app.context import build_project_context
from app.state import AgentState
from app.config import (
    MAX_TOOL_CALLS,
    MAX_HISTORY,
    DEBUG,
)
console = Console()


WRITE_TOOLS = {
    "write_file",
}

class Agent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]
        self.state = AgentState()

    def _trim_history(self):
        """
        Keep the system prompt and the most recent
        complete conversation turns.
    
        Supports both plain dictionaries and SDK
        ChatCompletionMessage objects.
        """
    
        if len(self.messages) <= MAX_HISTORY:
            return
    
        system = self.messages[0]
        history = self.messages[1:]
    
        def get_role(message):
            if isinstance(message, dict):
                return message.get("role")
    
            return getattr(message, "role", None)
    
        while len([system] + history) > MAX_HISTORY:
        
            # Find the oldest user message.
            while history and get_role(history[0]) != "user":
                history.pop(0)
    
            if not history:
                break
            
            # Remove the oldest user message.
            history.pop(0)
    
            # Remove everything belonging to that turn:
            # assistant/tool/assistant responses until
            # the next user message.
            while history and get_role(history[0]) != "user":
                history.pop(0)
    
        self.messages = [system] + history

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

    def _build_user_message(self, user_message: str) -> dict:
        """
        Build the user message with additional context when needed.
        """

        content = user_message

        project_keywords = [
            "project",
            "codebase",
            "repository",
        ]

        if any(word in user_message.lower() for word in project_keywords):

            content += (
                "\n\nPROJECT CONTEXT\n"
                + build_project_context()
            )

        return {
            "role": "user",
            "content": content,
        }

    def _call_llm(self) -> Any:
        """
        Send the current conversation to the LLM.
        """

        if DEBUG:

            total_chars = 0

            for msg in self.messages:

                if isinstance(msg, dict):

                    total_chars += len(
                        str(msg.get("content", ""))
                    )

                else:

                    total_chars += len(
                        str(getattr(msg, "content", ""))
                    )

            print("\n========== REQUEST DEBUG ==========")
            print(f"Messages   : {len(self.messages)}")
            print(f"Characters : {total_chars}")

            print("\nRoles:")

            for i, msg in enumerate(self.messages, start=1):

                if isinstance(msg, dict):
                    role = msg.get("role", "unknown")
                else:
                    role = getattr(msg, "role", "unknown")

                print(f"{i:02d}. {role}")

            print("===================================\n")

        try:

            return ask_llm(self.messages)

        except RuntimeError as e:

            self.state.last_error = str(e)

            return str(e)
    
    def _parse_arguments(self, tool_call) -> dict | None:
        """
        Parse tool arguments safely.
        """

        try:
            return json.loads(
                tool_call.function.arguments
            )

        except json.JSONDecodeError:
            return None

    def _execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ):
        """
        Execute a tool.
        """

        return execute(
            tool_name,
            arguments,
        )

    def _handle_tool_call(
        self,
        tool_call,
    ):
        """
        Execute a single tool call and
        store the result.
        """

        tool_name = tool_call.function.name

        self.state.tool_calls += 1
        self.state.last_tool = tool_name

        arguments = self._parse_arguments(tool_call)

        if arguments is None:

            self.state.last_error = (
                "The model returned invalid tool arguments."
            )

            return self.state.last_error

        if tool_name in WRITE_TOOLS:

            if not self._confirm_write(
                arguments.get("path", "")
            ):

                self.state.last_error = (
                    "Operation cancelled by user."
                )

                return self.state.last_error

        result = self._execute_tool(
            tool_name,
            arguments,
        )

        if not result.success:

            self.state.last_error = result.output

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

        return None


    def chat(self, user_message: str) -> str:
        """
        Process a user message using a multi-step
        tool-calling loop.
        """

        self.state.reset()
        self.messages.append(
            self._build_user_message(user_message)
        )

        for step in range(MAX_TOOL_CALLS):
            self.state.steps += 1
            reply = self._call_llm()

            if isinstance(reply, str):
                return reply

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

                error = self._handle_tool_call(tool_call)

                if error:
                    return error

        self._trim_history()

        return (
            "Maximum tool call limit reached. "
            "Unable to complete the request."
        )
