import json
import logging
import uuid
from datetime import datetime

from common.clients.dynamo import Dynamo
from common.threads.threads import call_with_threads
from lambdas.recommendations.models.book import BookRecommendationResponse
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import OpenAIWrapper


def get_recommendations_from_text(
    open_ai_wrapper: OpenAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    dynamo: Dynamo,
    user_input: str,
) -> str:
    open_ai_response = open_ai_wrapper.query(
        temperature=0.4,
        user_input=f"""
        You help people find books they might want to read. Recommend 7 books for '{user_input}'.
        Respond with JSON data containing book name and author [{{"t": "title", "a": "author"}}].
        Only include the JSON data.""",
    )
    try:
        open_ai_response_as_dict: list[dict] = json.loads(open_ai_response)
        google_books_responses = call_with_threads(
            function=google_books_wrapper.request_book,
            function_input=open_ai_response_as_dict,
        )
        response_data = BookRecommendationResponse(
            books=[response for response in google_books_responses if response],
            user_input=user_input,
        ).to_dict_by_alias()
        dynamo.store_in_dynamodb(
            {
                **response_data,
                "recommendation_id": str(uuid.uuid4()),
                "timestamp": str(datetime.utcnow().isoformat()),
            }
        )
        return json.dumps(response_data)
    except json.JSONDecodeError:
        logging.error(f"open ai response - {open_ai_response}")
        return json.dumps(
            BookRecommendationResponse(
                books=[],
                user_input=user_input,
            ).to_dict_by_alias()
        )
