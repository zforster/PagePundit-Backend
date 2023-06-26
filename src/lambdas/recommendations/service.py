import json
import logging
import uuid
from datetime import datetime
from decimal import Decimal

from common.threads.threads import call_with_threads
from lambdas.recommendations.models.book import BookRecommendationResponse
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
                "content": f"""You help people find books they might want to read. Respond ONLY with JSON data containing book name and author. E.g. [{{"t": "title", "a": "author"}}].""",
            },
            {
                "role": "user",
                "content": f"""Recommend a maximum of 15 books for '{user_input}'. Respond with JSON data containing book name and author only. Example response: [{{"t": "title", "a": "author"}}]. Do not respond with anything but the example JSON format, no other words.""",
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
    except json.JSONDecodeError as e:
        logging.error(f"open ai response - {open_ai_response}")
        raise Exception(e)


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
    open_ai_wrapper: OpenAIWrapper,
    recommendation_id: str,
    recommendation_repo: DynamoRecommendationRepo,
    index: int,
) -> str:
    recommendation = recommendation_repo.get_recommendation_by_id(
        recommendation_id=recommendation_id
    )
    book = recommendation.books[index]
    authors = "& ".join(book.authors)

    open_ai_response = open_ai_wrapper.chat(
        temperature=0.4,
        messages=[
            {
                "role": "user",
                "content": f"""
                In 70 words or less write a summary about the book {book.title} by {authors}.
                Only respond with the summary.""",
            },
        ],
    )
    return json.dumps({'data': open_ai_response})


def get_reason(
    open_ai_wrapper: OpenAIWrapper,
    recommendation_id: str,
    recommendation_repo: DynamoRecommendationRepo,
    index: int,
) -> str:
    recommendation = recommendation_repo.get_recommendation_by_id(
        recommendation_id=recommendation_id
    )
    book = recommendation.books[index]
    authors = "& ".join(book.authors)
    open_ai_response = open_ai_wrapper.chat(
        temperature=0.4,
        messages=[
            {
                "role": "user",
                "content": f"In 50 words or less explain to a person why {book.title} by {authors} will appeal to someone looking for {recommendation.user_input}. Reference the user's input in the response.",
            },
        ],
    )
    return json.dumps({'data': open_ai_response})
