from typing import Optional, TypedDict

import requests

from common.model.book import Book


class BookRequest(TypedDict):
    t: str
    a: str


class GoogleBooksWrapper:
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.BASE_URL = "https://www.googleapis.com/books/v1/"

    @staticmethod
    def get_thumbnail(images: dict) -> Optional[str]:
        if images == {}:
            return None
        return images.get("thumbnail").replace("&edge=curl", "")

    @staticmethod
    def get_amazon_url(title: str, authors: list) -> str:
        base = "s?k="
        if len(authors) > 0:
            return f'{base}{title}+{", ".join([author for author in authors])}&i=stripbooks'
        return f"{base}{title}&i=stripbooks"

    def request_book(self, book: BookRequest) -> Optional[Book]:
        url = f"{self.BASE_URL}volumes?q=intitle:{book['t']}+inauthor:{book['a']}&key={self.API_KEY}&printType=books&langRestrict=en"
        response = requests.get(url)
        response_json = response.json()
        response_items = response_json.get("items")

        if response_items is None:
            return None

        responses_with_images = [
            res
            for res in response_items
            if self.get_thumbnail(images=res["volumeInfo"].get("imageLinks", {}))
        ]

        if not responses_with_images:
            return None

        response_item = responses_with_images[0]

        volume_info = response_item["volumeInfo"]

        return Book(
            title=volume_info["title"],
            subtitle=volume_info.get("subtitle"),
            authors=volume_info.get("authors", []),
            publisher=volume_info.get("publisher"),
            publish_date=volume_info.get("publishedDate"),
            description=volume_info.get("description"),
            pages=volume_info.get("pageCount"),
            categories=volume_info.get("categories", []),
            average_rating=volume_info.get("averageRating"),
            total_ratings=volume_info.get("ratingsCount"),
            thumbnail_url=self.get_thumbnail(images=volume_info.get("imageLinks", {})),
            amazon_search_url=self.get_amazon_url(
                title=volume_info["title"], authors=volume_info.get("authors", [])
            ),
        )
