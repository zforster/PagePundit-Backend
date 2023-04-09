from typing import Optional

import boto3


class Dynamo:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def store_in_dynamodb(self, item: dict) -> None:
        self.table.put_item(Item=item)

    def paginate(
        self,
        key_condition_expression: str,
        expression_attribute: dict,
        exclusive_start_key: Optional[dict] = None,
        limit: Optional[int] = 10,
    ) -> dict:
        if exclusive_start_key is None:
            return self.table.query(
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_attribute,
                ScanIndexForward=False,
                Limit=limit,
            )
        return self.table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute,
            ExclusiveStartKey=exclusive_start_key,
            ScanIndexForward=False,
            Limit=limit,
        )
