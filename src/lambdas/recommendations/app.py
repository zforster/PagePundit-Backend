import json
from typing import Dict, Optional

import lambdas.recommendations.service as service_layer
from common.clients.parameter_store import get_google_books_api_key
from lambdas.recommendations.wrappers.google_books_wrapper import (
    AbstractGoogleBooksWrapper,
    GoogleBooksWrapper,
)
from lambdas.recommendations.wrappers.open_ai_wrapper import (
    AbstractOpenAIWrapper,
    MockOpenAIWrapper,
)


def get_category_recommendations(
    event: Dict,
    context: Dict,
    open_ai_wrapper: Optional[AbstractOpenAIWrapper] = None,
    google_books_wrapper: Optional[AbstractGoogleBooksWrapper] = None,
) -> Dict:
    if not open_ai_wrapper:
        open_ai_wrapper = MockOpenAIWrapper()

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=get_google_books_api_key())

    event_body = json.loads(event["body"])

    return {
        "statusCode": 200,
        "body": service_layer.get_category_recommendations(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            categories=event_body.get("categories"),
        ),
    }


def get_recommendations_from_book(
    event: Dict,
    context: Dict,
    open_ai_wrapper: Optional[AbstractOpenAIWrapper] = None,
    google_books_wrapper: Optional[GoogleBooksWrapper] = None,
) -> Dict:
    if not open_ai_wrapper:
        open_ai_wrapper = MockOpenAIWrapper()

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=get_google_books_api_key())

    event_body = json.loads(event["body"])

    return {
        "statusCode": 200,
        "body": service_layer.get_recommendations_from_book(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            book_name=event_body["name"],
            authors=event_body["authors"],
        ),
    }
