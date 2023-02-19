from typing import Optional

import lambdas.recommendations.service as service_layer
from common.clients.parameter_store import get_google_books_api_key, get_open_ai_api_key
from lambdas.recommendations.wrappers.google_books_wrapper import (
    AbstractGoogleBooksWrapper,
    GoogleBooksWrapper,
)
from lambdas.recommendations.wrappers.open_ai_wrapper import (
    AbstractOpenAIWrapper,
    OpenAIWrapper,
    MockOpenAIWrapper
)


def get_category_recommendations(
    event: dict,
    context: dict,
    open_ai_wrapper: Optional[AbstractOpenAIWrapper] = None,
    google_books_wrapper: Optional[AbstractGoogleBooksWrapper] = None,
) -> dict:
    """
    Gets book recommendations based on user category preferences
    """
    if not open_ai_wrapper:
        open_ai_wrapper = MockOpenAIWrapper()

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=get_google_books_api_key())

    query_params = event.get("queryStringParameters", {})

    return {
        "statusCode": 200,
        "body": service_layer.get_category_recommendations(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            category=query_params["category"],
        ),
    }


def get_recommendations_from_book(
    event: dict,
    context: dict,
    open_ai_wrapper: Optional[AbstractOpenAIWrapper] = None,
    google_books_wrapper: Optional[GoogleBooksWrapper] = None,
) -> dict:
    """
    Returns similar books to that being viewed by a particular user
    """
    if not open_ai_wrapper:
        open_ai_wrapper = MockOpenAIWrapper()

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=get_google_books_api_key())

    query_params = event.get("queryStringParameters", {})

    return {
        "statusCode": 200,
        "body": service_layer.get_recommendations_from_book(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            book_name=query_params["name"],
            authors=query_params["authors"].split(","),
        ),
    }
