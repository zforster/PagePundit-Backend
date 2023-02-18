from typing import Optional
from lambdas.categories.repo import S3CategoryRepo, BaseCategoryRepo
import json
import lambdas.categories.service as service_layer


def get_categories(
    event: dict,
    context: dict,
) -> dict:
    """
    Gets available categories a user can select as interests
    """
    return {
        "statusCode": 200,
        "body": service_layer.get_categories(),
    }


def post_categories(
    event: dict, context: dict, category_repo: Optional[BaseCategoryRepo] = None
) -> dict:
    """
    Stores a user category preferences
    """
    if category_repo is None:
        category_repo = S3CategoryRepo()
    service_layer.store_categories(
        category_repo=category_repo, categories=json.loads(event["body"]), user_id="zak"
    )
    return {
        "statusCode": 201,
    }
