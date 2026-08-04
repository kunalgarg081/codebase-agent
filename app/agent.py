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
        
        print("\n========== LLM RESPONSE ==========")
        print(reply)
        print("==================================\n")

        # Step 3 - No tool required

        if not reply.tool_calls:

            self.messages.append(reply)

            return reply.content

        # Step 4 - Execute first tool

        tool_call = reply.tool_calls[0]

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        result = execute(
            tool_name,
            arguments,
        )

        # Step 5 - Save assistant message

        self.messages.append(reply)

        # Step 6 - Send tool result

        self.messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            }
        )

        # Step 7 - Ask the LLM again

        final = ask_llm(self.messages)

        self.messages.append(final)

        return final.content