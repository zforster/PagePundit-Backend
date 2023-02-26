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
    average_rating: Optional[float] = None
    total_ratings: Optional[int] = None
    thumbnail_url: str
    amazon_search_url: str
