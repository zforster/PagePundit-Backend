from repo import BaseCategoryRepo, S3CategoryRepo

import lambdas.categories.service as service_layer


def get_categories(
    event: dict,
    context: dict,
) -> dict:
    return {
        "statusCode": 200,
        "body": service_layer.get_categories(),
    }


def post_categories(
    event: dict, context: dict, category_repo: BaseCategoryRepo
) -> dict:
    if category_repo is None:
        category_repo = S3CategoryRepo()
    service_layer.store_categories(category_repo=category_repo,
                                   categories=event["body"],
                                   user_id='zak')
    return {
        "statusCode": 201,
    }
