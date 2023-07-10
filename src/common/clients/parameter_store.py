import boto3

ssm = boto3.client("ssm")


def get_open_ai_api_key() -> str:
    return ssm.get_parameter(Name="open_ai_key")["Parameter"]["Value"]


def get_google_books_api_key() -> str:
    return ssm.get_parameter(Name="google_books_key")["Parameter"]["Value"]


def get_reddit_bot_username() -> str:
    return ssm.get_parameter(Name="reddit_bot_username")["Parameter"]["Value"]


def get_reddit_bot_password() -> str:
    return ssm.get_parameter(Name="reddit_bot_password")["Parameter"]["Value"]


def get_reddit_bot_client_id() -> str:
    return ssm.get_parameter(Name="reddit_bot_client_id")["Parameter"]["Value"]


def get_reddit_bot_client_secret() -> str:
    return ssm.get_parameter(Name="reddit_bot_secret")["Parameter"]["Value"]
