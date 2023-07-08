from os import environ

import boto3
from boto3.dynamodb.conditions import Key
from pydantic import parse_obj_as

from lambdas.recommendations.models.book import BookRecommendationResponse


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
