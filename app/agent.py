import json

from app.llm import ask_llm
from app.prompts import SYSTEM_PROMPT
from app.tool_executor import execute


class Agent:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

    def _parse_tool_call(self, content: str) -> dict | None:
        """
        Parse the LLM response and determine
        whether it is a valid tool call.
        """

        try:

            data = json.loads(content)

            if not isinstance(data, dict):
                return None

            if "tool" not in data:
                return None

            if "arguments" not in data:
                return None

            return data

        except json.JSONDecodeError:
            return None

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
        Process a user message and return
        the assistant response.
        """

        # Step 1 - Add user message

        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        # Step 2 - Ask the LLM

        reply = ask_llm(self.messages)

        tool_call = self._parse_tool_call(reply.content)

        # Step 3 - No tool required

        if tool_call is None:

            self.messages.append(reply)

            return reply.content

        # Step 4 - Execute tool

        result = execute(
            tool_call["tool"],
            tool_call["arguments"],
        )

        # Step 5 - Save assistant tool request

        self.messages.append(reply)

        # Step 6 - Send tool result back to LLM

        self.messages.append(
            {
                "role": "user",
                "content": self._tool_result_prompt(result),
            }
        )

        # Step 7 - Generate final answer

        final = ask_llm(self.messages)

        self.messages.append(final)

        return final.content