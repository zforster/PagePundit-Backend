from abc import ABC, abstractmethod

import requests

from lambdas.recommendations.models.book import Book


class AbstractGoogleBooksWrapper(ABC):
    @abstractmethod
    def request_book(
        self,
        title: str,
        author: str,
    ) -> Book:
        raise NotImplementedError


class MockGoogleBooksWrapper(AbstractGoogleBooksWrapper):
    def request_book(
        self,
        title: str,
        author: str,
    ) -> Book:
        return Book(
            title="The Dichotomy of Leadership",
            subtitle="Balancing the Challenges of Extreme Ownership to Lead and Win",
            authors=["Jocko Willink", "Leif Babin"],
            publisher="St. Martin's Press",
            publish_date="2018-09-25",
            description="THE INSTANT #1 NATIONAL BESTSELLER From the #1.",
            ISBN_10="1250195780",
            ISBN_13="9781250195784",
            pages=320,
            categories=["Business & Economics"],
            average_rating=3.5,
            total_ratings=2,
            thumbnail_url="http://books.google.com/books/content?id=DRtNDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api",
        )


class GoogleBooksWrapper(AbstractGoogleBooksWrapper):
    def __init__(self, api_key: str):
        self.API_KEY = api_key
        self.BASE_URL = "https://www.googleapis.com/books/v1/"

    def request_book(
        self,
        title: str,
        author: str,
    ) -> Book:
        response = requests.get(
            url=f"{self.BASE_URL}volumes?q=intitle:{title}+inauthor:{author}&key={self.API_KEY}"
        )
        response_item = response.json()["items"][0]
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
            thumbnail_url=volume_info.get("imageLinks", {"thumbnail": None}).get(
                "thumbnail"
            ),
        )
