from decimal import Decimal

import boto3


class Dynamo:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def convert_floats_to_decimal(self, d: dict) -> dict:
        for key, value in d.items():
            if isinstance(value, float):
                d[key] = Decimal(str(value))
            elif isinstance(value, dict):
                d[key] = self.convert_floats_to_decimal(value)
        return d

    def store_in_dynamodb(self, item: dict) -> None:
        self.table.put_item(Item=self.convert_floats_to_decimal(d=item))
