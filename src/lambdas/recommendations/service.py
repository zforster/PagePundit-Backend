import json

from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import AbstractOpenAIWrapper


def get_recommendations_from_text(
    open_ai_wrapper: AbstractOpenAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    user_input: str,
) -> str:
    open_ai_response = open_ai_wrapper.query(
        prompt=f"""
        Recommend 5 books maximum about {user_input}. 
        Respond in JSON with the keys title as t, author as a. 
        For example [{{ "t": title",  "a": "author"}}]."""
    )
    open_ai_response_as_dict = json.loads(open_ai_response)

    recommendations = []
    for book in open_ai_response_as_dict:
        book_data = google_books_wrapper.request_book(title=book["t"], author=book["a"])
        if book_data is not None:
            recommendations.append(book_data)

    return json.dumps([book.to_dict_by_alias() for book in recommendations])
