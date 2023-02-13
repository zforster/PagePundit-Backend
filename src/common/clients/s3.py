import json
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class S3:
    def __init__(
        self,
    ):
        self.s3_resource = boto3.resource(
            "s3",
        )
        self.s3_client = boto3.client(
            "s3",
        )

    def file_exists(self, bucket_name: str, file_name: str) -> bool:
        try:
            self.s3_client.head_object(Bucket=bucket_name, Key=file_name)
        except ClientError as e:
            return int(e.response["Error"]["Code"]) != 404
        return True

    def upload_object(self, bucket_name: str, file_name: str, file_body: str) -> None:
        return self.s3_resource.Object(bucket_name, file_name).put(Body=file_body)

    def query_file(
        self,
        bucket_name: str,
        file_name: str,
        query: Optional[str] = "select * from S3Object[*].payload[*]",
    ) -> List[Dict]:
        response = self.s3_client.select_object_content(
            Bucket=bucket_name,
            Key=file_name,
            ExpressionType="SQL",
            Expression=query,
            InputSerialization={
                "JSON": {"Type": "DOCUMENT"},
                "CompressionType": "NONE",
            },
            OutputSerialization={"JSON": {"RecordDelimiter": ","}},
        )
        records_str = ""
        for event in response["Payload"]:
            if "Records" in event:
                records_str = records_str + event["Records"]["Payload"].decode("utf-8")
        comma_sep_docs = records_str.replace("\n", ",")[:-1]
        return json.loads(f"[{comma_sep_docs}]")
