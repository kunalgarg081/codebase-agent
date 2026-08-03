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

    def _is_tool_call(self, content: str):
        try:
            data = json.loads(content)
    
            if not isinstance(data, dict):
                return None
    
            if "tool" not in data:
                return None
    
            return data
    
        except json.JSONDecodeError:
            return None

    def chat(self, user_message):

        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        reply = ask_llm(self.messages)

        content = reply.content

        tool_call = self._is_tool_call(content)

        if tool_call is None:
            self.messages.append(reply)
            return content

        result = execute(
            tool_call["tool"],
            tool_call["arguments"],
        )

        self.messages.append(reply)

        self.messages.append(
            {
                "role": "user",
                "content": f"""
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
""",
            }
        )

        final = ask_llm(self.messages)

        self.messages.append(final)

        return final.content