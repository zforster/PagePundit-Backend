import json
from abc import ABC
from os import environ

from common.clients.s3 import S3
from lambdas.categories.category import Category


class BaseCategoryRepo(ABC):
    def store_categories(self, categories: list[Category], user_id: str) -> None:
        raise NotImplementedError

    def get_categories(self, user_id: str) -> list[Category]:
        raise NotImplementedError


class S3CategoryRepo(BaseCategoryRepo):
    def __init__(
        self,
    ):
        self.s3 = S3()
        self.bucket = environ.get("CategoryBucket")

    @staticmethod
    def get_filename(user_id: str) -> str:
        return f"{user_id}.json"

    def store_categories(self, categories: list[Category], user_id: str) -> None:
        self.s3.upload_object(
            bucket_name=self.bucket,
            file_name=self.get_filename(user_id=user_id),
            file_body=json.dumps(
                [category.to_dict_by_alias() for category in categories]
            ),
        )

    def get_categories(self, user_id: str) -> list[Category]:
        data = self.s3.query_file(
            bucket_name=self.bucket,
            file_name=self.get_filename(user_id=user_id),
            query="select * from S3Object[*]",
        )
        return [Category(**category) for category in data[0]["_1"]]
