from enum import Enum
from typing import Optional, TypedDict

import openai


class Models(str, Enum):
    GPT_4O_MINI = "gpt-4o-mini"


class Message(TypedDict):
    role: str
    content: str


class OpenAIWrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def chat(
        self,
        messages: list[Message],
        temperature: Optional[float] = 0.7,
    ) -> str:
        openai.api_key = self.api_key
        completions = openai.ChatCompletion.create(
            model=Models.GPT_4O_MINI, temperature=temperature, messages=messages
        )
        return completions.choices[0]["message"]["content"]
