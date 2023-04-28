from decimal import Decimal
from typing import Optional

from common.model.base import SnakeToCamelCaseModel


class Book(SnakeToCamelCaseModel):
    title: str
    subtitle: Optional[str] = None
    authors: list[str]
    publisher: Optional[str] = None
    publish_date: Optional[str] = None
    description: Optional[str] = None
    pages: Optional[int] = None
    categories: list[str]
    average_rating: Optional[Decimal] = None
    total_ratings: Optional[int] = None
    thumbnail_url: Optional[str] = None
    amazon_search_url: str


class BookRecommendationResponse(SnakeToCamelCaseModel):
    recommendation_id: str
    user_input: str
    timestamp: str
    books: list[Book]


class ExclusiveStartKey(SnakeToCamelCaseModel):
    recommendation_type: str
    timestamp: str


class FetchBookRecommendationsResponse(SnakeToCamelCaseModel):
    recommendations: list[BookRecommendationResponse]
    exclusive_start_key: Optional[ExclusiveStartKey] = None
