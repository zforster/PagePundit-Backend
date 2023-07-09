from typing import Optional

from praw.reddit import Reddit

import common.clients.parameter_store as parameter_store
import lambdas.reddit.service as service_layer
from common.repository.recommendation import DynamoRecommendationRepo
from common.wrappers.google_books_wrapper import GoogleBooksWrapper
from common.wrappers.recommendation_wrapper import RecommendationAIWrapper

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


def post_reddit_recommendations(
    event: dict,
    context: dict,
    recommendation_wrapper: Optional[RecommendationAIWrapper] = None,
    google_books_wrapper: Optional[GoogleBooksWrapper] = None,
) -> dict:
    """
    Recommend books based on text input
    """
    if not recommendation_wrapper:
        recommendation_wrapper = RecommendationAIWrapper(api_key=parameter_store.get_open_ai_api_key())

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=parameter_store.get_google_books_api_key())

    return {
        "statusCode": 200,
        "headers": get_response_headers(event=event),
        "body": service_layer.make_reddit_responses(
            recommendation_wrapper=recommendation_wrapper,
            google_books_wrapper=google_books_wrapper,
            recommendation_repo=DynamoRecommendationRepo(),
            reddit_wrapper=Reddit(
                username=parameter_store.get_reddit_bot_username(),
                password=parameter_store.get_reddit_bot_password(),
                client_id=parameter_store.get_reddit_bot_client_id(),
                client_secret=parameter_store.get_reddit_bot_client_secret(),
                user_agent="PagePundit",
            )
        ),
    }
