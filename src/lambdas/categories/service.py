import json

from lambdas.categories.category import Category
from lambdas.categories.repo import BaseCategoryRepo
from lambdas.categories.utils import book_categories


def get_categories() -> str:
    return json.dumps(book_categories)


def store_categories(
    category_repo: BaseCategoryRepo, categories: list[dict], user_id: str
) -> None:
    category_repo.store_categories(
        categories=[Category(**category) for category in categories], user_id=user_id
    )


def get_user_selected_categories(category_repo: BaseCategoryRepo, user_id: str) -> str:
    return json.dumps(
        [c.to_dict_by_alias() for c in category_repo.get_categories(user_id=user_id)]
    )
