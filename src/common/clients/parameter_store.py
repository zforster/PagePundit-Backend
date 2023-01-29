import boto3

ssm = boto3.client("ssm")


def get_open_ai_api_key() -> str:
    return ssm.get_parameter(Name="open_ai_key")["Parameter"]["Value"]


def get_google_books_api_key() -> str:
    return ssm.get_parameter(Name="google_books_key")["Parameter"]["Value"]
