import json
import logging
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from common.threads.threads import call_with_threads
from lambdas.recommendations.models.book import (
    BookRecommendationResponse,
    ExclusiveStartKey,
)
from lambdas.recommendations.repository.recommendation import DynamoRecommendationRepo
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import OpenAIWrapper


def get_recommendations_from_text(
    open_ai_wrapper: OpenAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    recommendation_repo: DynamoRecommendationRepo,
    user_input: str,
) -> str:
    open_ai_response = open_ai_wrapper.chat(
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": "You help people find books they might want to read.",
            },
            {
                "role": "user",
                "content": f"""Recommend 6 books for '{user_input}'. Respond with JSON data containing book name, author and short reason as to why you think it is a good fit under 20 words. [{{"t": "title", "a": "author", "r": "reason"}}]. Only include the JSON data.""",
            },
        ],
    )
    try:
        recommendation_id = str(uuid.uuid4())
        open_ai_response_as_dict: list[dict] = json.loads(open_ai_response)
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
            raise Exception('No recommendations found')

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
    except json.JSONDecodeError as e:
        logging.error(f"open ai response - {open_ai_response}")
        raise Exception(e)


def read_recommendations(
    recommendation_repo: DynamoRecommendationRepo,
    exclusive_start_key: Optional[ExclusiveStartKey] = None,
) -> str:
    return json.dumps(
        recommendation_repo.fetch_recommendations(
            exclusive_start_key=exclusive_start_key
        ).to_dict_by_alias(),
        default=float,
    )


def get_recommendation_by_id(
    recommendation_repo: DynamoRecommendationRepo, recommendation_id: str
) -> str:
    return json.dumps(
        recommendation_repo.get_recommendation_by_id(
            recommendation_id=recommendation_id
        ).to_dict_by_alias(),
        default=float,
    )
