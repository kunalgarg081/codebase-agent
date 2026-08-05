from typing import Any

from openai import OpenAI

from app.config import API_KEY, BASE_URL, MODEL
from app.tools import TOOL_SCHEMAS


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def ask_llm(messages: list[dict[str, Any]]):
    """
    Send the conversation to the LLM and
    return the assistant message.
    """

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            temperature=0.2,
        )

        return response.choices[0].message

    except Exception as e:
        raise RuntimeError(
            f"LLM request failed: {e}"
        ) from e