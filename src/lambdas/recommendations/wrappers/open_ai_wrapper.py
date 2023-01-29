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
              { "t": "The Dichotomy of Leadership", "a": "Jocko Willink and Leif Babin" },
              { "t": "The Hard Thing About Hard Things", "a": "Ben Horowitz" },
              { "t": "The Art of War", "a": "Sun Tzu" },
              { "t": "Start With Why", "a": "Simon Sinek" },
              { "t": "Leaders Eat Last", "a": "Simon Sinek" }
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
