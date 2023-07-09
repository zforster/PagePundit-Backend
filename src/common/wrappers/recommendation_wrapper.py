import json
import logging

from common.wrappers.open_ai_wrapper import OpenAIWrapper


class InvalidResponseException(Exception):
    pass


class RecommendationAIWrapper:
    def __init__(self, api_key: str):
        self.open_ai_wrapper = OpenAIWrapper(api_key=api_key)

    def get_book_recommendations_from_text(
        self, user_input: str, recommendation_count: int
    ) -> list[dict]:
        open_ai_response = self.open_ai_wrapper.chat(
            temperature=0.4,
            messages=[
                {
                    "role": "system",
                    "content": f"""You help people find books they might want to read. Respond ONLY with JSON data containing book name and author. E.g. [{{"t": "title", "a": "author"}}].""",
                },
                {
                    "role": "user",
                    "content": f"""Recommend a maximum of {recommendation_count} books for '{user_input}'. Respond with JSON data containing book name and author only. Example response: [{{"t": "title", "a": "author"}}]. Do not respond with anything but the example JSON format, no other words.""",
                },
            ],
        )
        try:
            open_ai_response_as_dict: list[dict] = json.loads(open_ai_response)
            return open_ai_response_as_dict
        except json.JSONDecodeError as e:
            logging.error(f"open ai response - {open_ai_response}")
            raise InvalidResponseException(e)

    def get_book_summary(self, title: str, authors: str) -> str:
        return self.open_ai_wrapper.chat(
            temperature=0.4,
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        In 60 words or less write a summary about the book {title} by {authors}.
                        Only respond with the summary.""",
                },
            ],
        )

    def get_recommendation_reason(
        self, title: str, authors: str, user_input: str
    ) -> str:
        return self.open_ai_wrapper.chat(
            temperature=0.4,
            messages=[
                {
                    "role": "user",
                    "content": f"In 50 words or less explain to a person why {title} by {authors} will appeal to someone looking for {user_input}. Reference the user's input in the response.",
                },
            ],
        )

    def summarise_user_input(self, title: str, body: str) -> str:
        return self.open_ai_wrapper.chat(
            temperature=0.4,
            messages=[
                {
                    "role": "system",
                    "content": "You must summarise user input into a short sentance that can be passed into a system that uses natrual text to recommend books. Write in the perspective of the user, e.g 'I am looking for'",
                },
                {
                    "role": "user",
                    "content": f"summarise the following: {title} {body}",
                },
            ],
        )
