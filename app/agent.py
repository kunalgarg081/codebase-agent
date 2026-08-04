import json

from app.llm import ask_llm
from app.prompts import SYSTEM_PROMPT
from app.tool_executor import execute

MAX_TOOL_CALLS = 5
class Agent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    
    def _tool_result_prompt(self, result: str) -> str:
        """
        Create the follow-up prompt after
        executing a tool.
        """

        return f"""
Tool Result

{result}

Answer the user's request using the tool result.

If the user requested a code review, include:

1. Overall Score (out of 10)
2. Strengths
3. Weaknesses
4. Suggestions
5. Refactored Example (if useful)

If the user requested something else,
answer normally.
"""


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

        for _ in range(MAX_TOOL_CALLS):

            reply = ask_llm(self.messages)
            print(f"\n--- Tool Calls: {len(reply.tool_calls or [])} ---")
            # No more tool calls -> Final Answer
            if not reply.tool_calls:

                self.messages.append(reply)

                return reply.content

            # Save assistant message containing tool calls
            self.messages.append(reply)

            # Execute every requested tool
            for tool_call in reply.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                result = execute(
                    tool_name,
                    arguments,
                )
                print(f"Executed: {tool_name}({arguments})")
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    }
                )

        return (
            "Maximum tool call limit reached. "
            "Unable to complete the request."
        )