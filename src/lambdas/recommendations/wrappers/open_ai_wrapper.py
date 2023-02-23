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
        [{"t": "Alcohol: How to Give It Up and Be Happy", "a": "Linda R. Watson, M.D."}, 
        {"t": "The Alcohol Experiment: A 30-Day, Alcohol-Free Challenge to Interrupt Your Habits and Help You Take Control", "a": "Ariane Resnick"}, 
        {"t": "How To Stop Drinking Alcohol: A Simple Path From Alcohol Misuse to Alcohol Recovery", "a": "John M. Green"}, 
        {"t": "The Easy Way to Stop Drinking: Join the Millions Who Have Discovered How to Quit and Stay Quit", "a": "Allen Carr"}, 
        {"t": "The Alcoholic Family in Recovery: A Developmental Approach", "a": "Stephanie Brown"}]
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
