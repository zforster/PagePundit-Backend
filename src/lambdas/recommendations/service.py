import json
import uuid
from datetime import datetime
from decimal import Decimal

from common.model.book import BookRecommendationResponse
from common.repository.recommendation import DynamoRecommendationRepo
from common.threads.threads import call_with_threads
from common.wrappers.google_books_wrapper import GoogleBooksWrapper
from common.wrappers.recommendation_wrapper import RecommendationAIWrapper


def get_recommendations_from_text(
    recommendation_wrapper: RecommendationAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    recommendation_repo: DynamoRecommendationRepo,
    user_input: str,
) -> str:
    open_ai_response_as_dict = (
        recommendation_wrapper.get_book_recommendations_from_text(
            user_input=user_input, recommendation_count=10
        )
    )

    recommendation_id = str(uuid.uuid4())
    google_books_responses = call_with_threads(
        function=google_books_wrapper.request_book,
        function_input=open_ai_response_as_dict,
    )

    seen_names = set()
    books = []
    for book in google_books_responses:
        if not book:
            continue
        book_hash = f"{book.title}{book.subtitle}"
        if book_hash not in seen_names and book:
            books.append(book)
            seen_names.add(book_hash)

    if not books:
        raise Exception("No recommendations found")

    sorted_books = sorted(
        books, key=lambda b: b.average_rating or Decimal(0), reverse=True
    )

    recommendation_data = BookRecommendationResponse(
        recommendation_id=recommendation_id,
        books=sorted_books,
        user_input=user_input,
        timestamp=str(datetime.utcnow().isoformat()),
    )
    recommendation_repo.store_recommendation(recommendation=recommendation_data)
    return json.dumps(recommendation_data.to_dict_by_alias(), default=float)


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
