import json
from abc import ABC
from os import environ

from lambdas.categories.category import Category

from common.clients.s3 import S3


class BaseCategoryRepo(ABC):
    def store_categories(self, categories: list[Category], user_id: str) -> None:
        raise NotImplementedError


class S3CategoryRepo(BaseCategoryRepo):
    def __init__(
        self,
    ):
        self.s3 = S3()
        self.bucket = environ.get("CategoryBucket")

    def store_categories(self, categories: list[Category], user_id: str) -> None:
        file_name = f"{user_id}.json"
        self.s3.upload_object(
            bucket_name=self.bucket,
            file_name=file_name,
            file_body=json.dumps(
                [category.to_dict_by_alias() for category in categories]
            ),
        )
