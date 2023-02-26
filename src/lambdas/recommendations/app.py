from typing import Optional

import lambdas.recommendations.service as service_layer
from common.clients.parameter_store import get_google_books_api_key, get_open_ai_api_key
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import (
    MockOpenAIWrapper,
    OpenAIWrapper,
)


def get_recommendations_from_text(
    event: dict,
    context: dict,
    open_ai_wrapper: Optional[MockOpenAIWrapper] = None,
    google_books_wrapper: Optional[GoogleBooksWrapper] = None,
) -> dict:
    """
    Recommend books based on text input
    """
    if not open_ai_wrapper:
        open_ai_wrapper = MockOpenAIWrapper()

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=get_google_books_api_key())

    return {
        "statusCode": 200,
        "body": service_layer.get_recommendations_from_text(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            user_input=event["body"],
        ),
    }
