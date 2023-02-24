from typing import Optional

import requests

from lambdas.recommendations.models.book import Book


class GoogleBooksWrapper:
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.BASE_URL = "https://www.googleapis.com/books/v1/"

    @staticmethod
    def get_thumbnail(images: dict) -> Optional[str]:
        if images == {}:
            return None
        return images.get('thumbnail').replace("&edge=curl", "")

    def request_book(
        self,
        title: str,
        author: str,
    ) -> Optional[Book]:
        response = requests.get(
            url=f"{self.BASE_URL}volumes?q=intitle:{title}+inauthor:{author}&key={self.API_KEY}"
        )
        response_json = response.json()
        response_items = response_json.get("items")

        if response_items is None:
            return None

        response_item = response_items[0]

        volume_info = response_item["volumeInfo"]
        identifiers = volume_info["industryIdentifiers"]
        isbn_10 = [
            value["identifier"] for value in identifiers if value["type"] == "ISBN_10"
        ]
        isbn_13 = [
            value["identifier"] for value in identifiers if value["type"] == "ISBN_13"
        ]

        return Book(
            title=volume_info.get("title"),
            subtitle=volume_info.get("subtitle"),
            authors=volume_info.get("authors", []),
            publisher=volume_info.get("publisher"),
            publish_date=volume_info.get("publishedDate"),
            description=volume_info.get("description"),
            ISBN_10=isbn_10[0] if len(isbn_10) == 1 else None,
            ISBN_13=isbn_13[0] if len(isbn_13) == 1 else None,
            pages=volume_info.get("pageCount"),
            categories=volume_info.get("categories", []),
            average_rating=volume_info.get("averageRating"),
            total_ratings=volume_info.get("ratingsCount"),
            thumbnail_url=self.get_thumbnail(images=volume_info.get("imageLinks", {})),
            amazon_url='test'
        )
