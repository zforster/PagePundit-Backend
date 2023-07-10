import json

import common.logic.recommendation as shared_logic
from common.repository.recommendation import DynamoRecommendationRepo
from common.wrappers.google_books_wrapper import GoogleBooksWrapper
from common.wrappers.recommendation_wrapper import RecommendationAIWrapper


def get_recommendations_from_text(
    recommendation_wrapper: RecommendationAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    recommendation_repo: DynamoRecommendationRepo,
    user_input: str,
) -> str:
    new_recommendations = shared_logic.get_and_store_recommendations_from_text(
        recommendation_repo=recommendation_repo,
        user_input=user_input,
        recommendation_wrapper=recommendation_wrapper,
        google_books_wrapper=google_books_wrapper,
    )
    return json.dumps(new_recommendations.to_dict_by_alias(), default=float)


def get_recommendation_by_id(
    recommendation_repo: DynamoRecommendationRepo, recommendation_id: str
) -> str:
    return json.dumps(
        recommendation_repo.get_recommendation_by_id(
            recommendation_id=recommendation_id
        ).to_dict_by_alias(),
        default=float,
    )


def get_book_summary(
    recommendation_wrapper: RecommendationAIWrapper,
    recommendation_id: str,
    recommendation_repo: DynamoRecommendationRepo,
    index: int,
) -> str:
    recommendation = recommendation_repo.get_recommendation_by_id(
        recommendation_id=recommendation_id
    )
    book = recommendation.books[index]
    authors = "& ".join(book.authors)

    return json.dumps(
        {
            "data": recommendation_wrapper.get_book_summary(
                title=book.title, authors=authors
            )
        }
    )


def get_reason(
    recommendation_wrapper: RecommendationAIWrapper,
    recommendation_id: str,
    recommendation_repo: DynamoRecommendationRepo,
    index: int,
) -> str:
    recommendation = recommendation_repo.get_recommendation_by_id(
        recommendation_id=recommendation_id
    )
    book = recommendation.books[index]
    authors = "& ".join(book.authors)
    return json.dumps(
        {
            "data": recommendation_wrapper.get_recommendation_reason(
                title=book.title, authors=authors, user_input=recommendation.user_input
            )
        }
    )


def get_latest_recommendation(recommendation_repo: DynamoRecommendationRepo) -> str:
    return json.dumps(
        recommendation_repo.get_latest_recommendation().to_dict_by_alias(),
        default=float,
    )
