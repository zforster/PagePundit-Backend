import json

from lambdas.recommendations.wrappers.google_books_wrapper import (
    AbstractGoogleBooksWrapper,
)
from lambdas.recommendations.wrappers.open_ai_wrapper import AbstractOpenAIWrapper


def get_category_recommendations(
    category: str,
    open_ai_wrapper: AbstractOpenAIWrapper,
    google_books_wrapper: AbstractGoogleBooksWrapper,
) -> str:
    prompt = f'Recommend 3 books in category {category}. ' \
             f'Respond in JSON with the keys title as t, author as a. For example [{{ "t": title",  "a": "author"}}].'
    open_ai_response = open_ai_wrapper.query(prompt=prompt)
    open_ai_response_as_dict = json.loads(open_ai_response)
    return json.dumps(
        [
            google_books_wrapper.request_book(
                title=book["t"], author=book["a"]
            ).to_dict_by_alias()
            for book in open_ai_response_as_dict
        ]
    )


def get_recommendations_from_book(
    book_name: str,
    authors: list[str],
    open_ai_wrapper: AbstractOpenAIWrapper,
    google_books_wrapper: AbstractGoogleBooksWrapper,
) -> str:
    open_ai_response = open_ai_wrapper.query(
        prompt=f"""
        Recommend 5 books similar to {book_name} by {", ".join([author for author in authors])}. 
        Respond in JSON with the keys name as n, author as a. 
        For example [{{ "n": name",  "a": "author"}}]."""
    )
    open_ai_response_as_dict = json.loads(open_ai_response)
    return json.dumps(
        [
            google_books_wrapper.request_book(
                title=book["t"], author=book["a"]
            ).to_dict_by_alias()
            for book in open_ai_response_as_dict
        ]
    )
