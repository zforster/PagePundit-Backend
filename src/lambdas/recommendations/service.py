import json
import logging

from common.threads.threads import call_with_threads
from lambdas.recommendations.models.book import BookRecommendationResponse
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import OpenAIWrapper


def get_recommendations_from_text(
    open_ai_wrapper: OpenAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    user_input: str,
) -> str:
    open_ai_response = open_ai_wrapper.query(
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": """You are book recommendation engine. Only respond with JSON data containing book name and author [{{'t": "title", "a": "author"}}]."""
            },
            {
                "role": "user",
                "content": f"""Recommend 5 book for {user_input}. Only respond with JSON data containing book name and author [{{"t": "title", "a": "author"}}]. Do not include anything else other than JSON data.""",
            },
        ],
    )
    try:
        open_ai_response_as_dict: list[dict] = json.loads(open_ai_response)
        google_books_responses = call_with_threads(
            function=google_books_wrapper.request_book,
            function_input=open_ai_response_as_dict,
        )
        return json.dumps(
            BookRecommendationResponse(
                books=[response for response in google_books_responses if response],
                user_input=user_input,
            ).to_dict_by_alias()
        )
    except json.JSONDecodeError:
        logging.error(f"open ai response - {open_ai_response}")
        return json.dumps(
            BookRecommendationResponse(
                books=[],
                user_input=user_input,
            ).to_dict_by_alias()
        )
