import json
import logging

from common.threads.threads import call_with_threads
from lambdas.recommendations.models.book import Book
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import AbstractOpenAIWrapper


def get_recommendations_from_text(
    open_ai_wrapper: AbstractOpenAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    user_input: str,
) -> str:
    open_ai_response = open_ai_wrapper.query(
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": """
                You are book recommendation engine that replies incredibly fast. 
                You must reply in under 2 seconds. 
                You only respond with JSON data containing the book name and author [{{"t": "title", "a": "author"}}].
                """,
            },
            {
                "role": "user",
                "content": f"""
                Recommend 7 books for this input '{user_input}'.
                You must ONLY respond with JSON data containing the book name and author [{{"t": "title", "a": "author"}}].
                Do not include anything else other than JSON data.
                """,
            },
        ],
    )
    try:
        open_ai_response_as_dict: list[dict] = json.loads(open_ai_response)
        google_books_responses = call_with_threads(
            function=google_books_wrapper.request_book,
            function_input=open_ai_response_as_dict,
        )
        google_books_responses: list[Book] = [
            response for response in google_books_responses if response
        ]
        return json.dumps([book.to_dict_by_alias() for book in google_books_responses])
    except json.JSONDecodeError:
        logging.error(f"open ai response - {open_ai_response}")
        return "[]"
