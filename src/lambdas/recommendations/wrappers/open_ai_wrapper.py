from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

import openai


class Models(str, Enum):
    DAVINCI = "text-davinci-003"


class AbstractOpenAIWrapper(ABC):
    @abstractmethod
    def query(
        self,
        prompt: str,
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000,
    ) -> str:
        raise NotImplementedError


class MockOpenAIWrapper(AbstractOpenAIWrapper):
    def query(
        self,
        prompt: str,
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000,
    ) -> str:
        return """
        [ 
            {"t": "Steve Jobs",  "a": "Walter Isaacson"},
            {"t": "The Innovators: How a Group of Hackers, Geniuses, and Geeks Created the Digital Revolution",  "a": "Walter Isaacson"},
            {"t": "The Microsoft Way: The Real Story of How the Company Outsmarts Its Competition",  "a": "Randall Stross"},
            {"t": "The Google Story",  "a": "David A. Vise and Mark Malseed"},
            {"t": "Competing on Internet Time: Lessons from Netscape and Its Battle with Microsoft",  "a": "Michael A. Cusumano and David B. Yoffie"}
        ]
        """


class OpenAIWrapper(AbstractOpenAIWrapper):
    def __init__(self, api_key: str, engine: Optional[Models] = Models.DAVINCI.value):
        openai.api_key = api_key
        self.ENGINE = engine

    def query(
        self,
        prompt: str,
        temperature: Optional[float] = 0.7,
        max_tokens: Optional[int] = 1000,
    ) -> str:
        completion = openai.Completion.create(
            engine=self.ENGINE,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            temperature=temperature,
        )
        return completion.choices[0].text
