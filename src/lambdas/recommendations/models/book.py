from typing import Optional

from humps import camelize
from pydantic import BaseModel


class SnakeToCamelCaseModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True

    def to_json_by_alias(self) -> str:
        return self.json(by_alias=True)


class Book(SnakeToCamelCaseModel):
    title: str
    subtitle: Optional[str] = None
    authors: list[str]
    publisher: Optional[str] = None
    publish_date: str
    description: str
    ISBN_10: Optional[str] = None
    ISBN_13: Optional[str] = None
    pages: int
    categories: list[str]
    average_rating: Optional[float] = None
    total_ratings: Optional[int] = None
    thumbnail_url: Optional[str] = None
