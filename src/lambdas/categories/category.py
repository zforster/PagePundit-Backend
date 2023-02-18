from common.model.base import SnakeToCamelCaseModel


class Category(SnakeToCamelCaseModel):
    category: str
    subcategories: list[str]
