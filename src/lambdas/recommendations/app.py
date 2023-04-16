import json
import os
from typing import Optional

from pydantic import parse_obj_as

import lambdas.recommendations.service as service_layer
from common.clients.dynamo import Dynamo
from common.clients.parameter_store import get_google_books_api_key, get_open_ai_api_key
from lambdas.recommendations.models.book import ExclusiveStartKey
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import OpenAIWrapper

RECOMMENDATIONS_TABLE = Dynamo(table_name=os.environ["RECOMMENDATIONS_TABLE"])


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
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET",
        },
        "body": service_layer.get_recommendations_from_text(
            open_ai_wrapper=open_ai_wrapper,
            google_books_wrapper=google_books_wrapper,
            dynamo=RECOMMENDATIONS_TABLE,
            user_input=event["body"],
        ),
    }


def fetch_recommendations(
    event: dict,
    context: dict,
) -> dict:
    """
    Fetch stored recommendations in batches of 10
    """
    start_key = json.loads(event["body"])["exclusiveStartKey"]
    if start_key is None:
        exclusive_start_key = None
    else:
        exclusive_start_key = parse_obj_as(
            ExclusiveStartKey,
            {**start_key},
        )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET",
        },
        "body": service_layer.read_recommendations(
            dynamo=RECOMMENDATIONS_TABLE, exclusive_start_key=exclusive_start_key
        ),
    }
