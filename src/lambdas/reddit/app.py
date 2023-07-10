from typing import Optional

from praw.reddit import Reddit

import common.clients.parameter_store as parameter_store
import lambdas.reddit.service as service_layer
from common.repository.recommendation import DynamoRecommendationRepo
from common.wrappers.google_books_wrapper import GoogleBooksWrapper
from common.wrappers.recommendation_wrapper import RecommendationAIWrapper


def post_reddit_recommendations(
    event: dict,
    context: dict,
    recommendation_wrapper: Optional[RecommendationAIWrapper] = None,
    google_books_wrapper: Optional[GoogleBooksWrapper] = None,
) -> None:
    """
    Reply to reddit posts with recommendations bot
    """
    if not recommendation_wrapper:
        recommendation_wrapper = RecommendationAIWrapper(api_key=parameter_store.get_open_ai_api_key())

    if not google_books_wrapper:
        google_books_wrapper = GoogleBooksWrapper(api_key=parameter_store.get_google_books_api_key())

    service_layer.make_reddit_responses(
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
        )
