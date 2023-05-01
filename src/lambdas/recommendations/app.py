from typing import Optional

from pydantic import parse_obj_as

import lambdas.recommendations.service as service_layer
from common.clients.parameter_store import get_google_books_api_key, get_open_ai_api_key
from lambdas.recommendations.models.book import ExclusiveStartKey
from lambdas.recommendations.repository.recommendation import DynamoRecommendationRepo
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import OpenAIWrapper

ORIGINS = {'http://localhost:3000', 'https://zforster.github.io'}


def get_response_headers(event: dict) -> dict:
    request_origin = event['headers']['origin']
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


def get_recommendations(
    event: dict,
    context: dict,
) -> dict:
    """
    Fetch stored recommendations in batches of 10
    """
    timestamp = event["pathParameters"]["timestamp"]
    recommendation_type = event["pathParameters"]["recommendation_type"]
    if timestamp is None:
        exclusive_start_key = None
    else:
        exclusive_start_key = parse_obj_as(
            ExclusiveStartKey,
            {"recommendation_type": recommendation_type, "timestamp": timestamp},
        )

    return {
        "statusCode": 200,
        "headers": get_response_headers(event=event),
        "body": service_layer.read_recommendations(
            recommendation_repo=DynamoRecommendationRepo(),
            exclusive_start_key=exclusive_start_key,
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
