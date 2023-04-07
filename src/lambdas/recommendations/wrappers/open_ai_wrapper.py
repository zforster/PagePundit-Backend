from enum import Enum
from typing import Optional, TypedDict

import openai


class Models(str, Enum):
    GTP_TURBO = "gpt-3.5-turbo"


class Message(TypedDict):
    role: str
    content: str


class OpenAIWrapper:
    def __init__(self, api_key: str, engine: Optional[Models] = Models.GTP_TURBO.value):
        openai.api_key = api_key
        self.ENGINE = engine

    def query(
        self,
        messages: list[Message],
        temperature: Optional[float] = 0.7,
    ) -> str:
        return openai.ChatCompletion.create(
            model=self.ENGINE, temperature=temperature, messages=messages
        ).choices[0]["message"]["content"]
