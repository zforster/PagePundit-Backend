from enum import Enum
from typing import Optional, TypedDict

import openai


class Models(str, Enum):
    GTP_TURBO = "gpt-3.5-turbo"
    DAVINCI = "text-davinci-003"


class Message(TypedDict):
    role: str
    content: str


class OpenAIWrapper:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def query(self, user_input: str, temperature: Optional[float] = 0.7) -> str:
        openai.api_key = self.api_key
        completions = openai.Completion.create(
            model=Models.DAVINCI,
            temperature=temperature,
            prompt=user_input,
            max_tokens=1000,
            n=1,
        )
        return completions["choices"][0]["text"]

    def chat(
        self,
        messages: list[Message],
        temperature: Optional[float] = 0.7,
    ) -> str:
        openai.api_key = self.api_key
        completions = openai.ChatCompletion.create(
            model=Models.GTP_TURBO, temperature=temperature, messages=messages
        )
        return completions.choices[0]["message"]["content"]
