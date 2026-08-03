from openai import OpenAI

from app.config import API_KEY, BASE_URL, MODEL

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)


def ask_llm(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message