import json

from models.category import Category
from repo import BaseCategoryRepo
from utils import book_categories


def get_categories() -> str:
    return json.dumps(book_categories)


def store_categories(
    category_repo: BaseCategoryRepo, categories: list[dict], user_id: str
) -> None:
    category_repo.store_categories(
        categories=[Category(**category) for category in categories], user_id=user_id
    )
