from os import environ
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key
from pydantic import parse_obj_as

from lambdas.recommendations.models.book import (
    BookRecommendationResponse,
    ExclusiveStartKey,
    FetchBookRecommendationsResponse,
)


class DynamoRecommendationRepo:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(environ["RECOMMENDATIONS_TABLE"])

    def store_recommendation(self, recommendation: BookRecommendationResponse) -> None:
        self.table.put_item(
            Item={
                **recommendation.dict(),
                "recommendation_type": "search",
                "recommendation_id": recommendation.recommendation_id,
            }
        )

    def fetch_recommendations(
        self, exclusive_start_key: Optional[ExclusiveStartKey] = None
    ) -> FetchBookRecommendationsResponse:
        results = self.table.query(
            KeyConditionExpression="recommendation_type = :type",
            ExpressionAttributeValues={":type": "search"},
            ExclusiveStartKey=exclusive_start_key.dict()
            if exclusive_start_key
            else None,
            ScanIndexForward=False,
            Limit=5,
        )

        response = parse_obj_as(
            FetchBookRecommendationsResponse,
            {
                "recommendations": results["Items"],
                "exclusive_start_key": results.get("LastEvaluatedKey"),
            },
        )

        return response

    def get_recommendation_by_id(
        self, recommendation_id: str
    ) -> BookRecommendationResponse:
        results = self.table.query(
            IndexName="RecommendationIdIndex",
            KeyConditionExpression=Key("recommendation_id").eq(recommendation_id),
        )

        response = parse_obj_as(
            BookRecommendationResponse,
            results["Items"][0],
        )

        return response
