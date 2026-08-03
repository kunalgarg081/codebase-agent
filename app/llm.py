from openai import OpenAI
from typing import Any
from app.config import API_KEY, BASE_URL, MODEL

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def ask_llm(messages: list[dict[str, Any]]):
    """
    Send a chat conversation to the LLM
    and return the assistant message.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
        )

    except Exception as e:
        raise RuntimeError(f"LLM request failed: {e}") from e

    return response.choices[0].message