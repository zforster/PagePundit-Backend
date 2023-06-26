from typing import Optional

import lambdas.recommendations.service as service_layer
from common.clients.parameter_store import get_google_books_api_key, get_open_ai_api_key
from lambdas.recommendations.repository.recommendation import DynamoRecommendationRepo
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import OpenAIWrapper

ORIGINS = {"https://pagepundit.com", "http://localhost:3000"}


def get_response_headers(event: dict) -> dict:
    request_origin = event["headers"].get("origin")
    response_origin = None
    for origin in ORIGINS:
        if origin == request_origin:
            response_origin = origin
    return {
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Origin": response_origin,
        "Access-Control-Allow-Methods": "GET",
    }


def get_recommendations_from_text(
    event: dict,
    context: dict,
    open_ai_wrapper: Optional[OpenAIWrapper] = None,
    google_books_wrapper: Optional[GoogleBooksWrapper] = None,
) -> dict:
    """
    Recommend books based on text input
    """
    if not open_ai_wrapper:
        open_ai_wrapper = OpenAIWrapper(api_key=get_open_ai_api_key())

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=get_google_books_api_key())

    return {
        "statusCode": 200,
        "headers": get_response_headers(event=event),
        "body": service_layer.get_recommendations_from_text(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            recommendation_repo=DynamoRecommendationRepo(),
            user_input=event["body"],
        ),
    }


def get_recommendation_by_id(event: dict, context: dict) -> dict:
    """
    Get recommendation by id
    """
    recommendation_id = event["pathParameters"]["recommendation_id"]
    return {
        "statusCode": 200,
        "headers": get_response_headers(event=event),
        "body": service_layer.get_recommendation_by_id(
            recommendation_id=recommendation_id,
            recommendation_repo=DynamoRecommendationRepo(),
        ),
    }


def get_book_summary(
    event: dict, context: dict, open_ai_wrapper: Optional[OpenAIWrapper] = None
) -> dict:
    """
    Get book summary
    """
    if not open_ai_wrapper:
        open_ai_wrapper = OpenAIWrapper(api_key=get_open_ai_api_key())

    recommendation_id = event["pathParameters"]["recommendation_id"]
    index = event["pathParameters"]["index"]
    return {
        "statusCode": 200,
        "headers": get_response_headers(event=event),
        "body": service_layer.get_book_summary(
            recommendation_id=recommendation_id,
            recommendation_repo=DynamoRecommendationRepo(),
            open_ai_wrapper=open_ai_wrapper,
            index=int(index),
        ),
    }


def get_reason(
    event: dict, context: dict, open_ai_wrapper: Optional[OpenAIWrapper] = None
) -> dict:
    """
    Get a reason someone would want to read the book based off their user input
    """
    if not open_ai_wrapper:
        open_ai_wrapper = OpenAIWrapper(api_key=get_open_ai_api_key())

    recommendation_id = event["pathParameters"]["recommendation_id"]
    index = event["pathParameters"]["index"]
    return {
        "statusCode": 200,
        "headers": get_response_headers(event=event),
        "body": service_layer.get_reason(
            recommendation_id=recommendation_id,
            recommendation_repo=DynamoRecommendationRepo(),
            open_ai_wrapper=open_ai_wrapper,
            index=int(index),
        ),
    }
