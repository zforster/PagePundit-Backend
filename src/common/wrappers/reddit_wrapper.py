import praw
from praw.models.reddit.submission import Submission


class RedditWrapper:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        username: str,
        password: str,
    ):
        self.praw = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            # username=username,
            # password=password,
        )

    def get_new_posts(self, subreddit: str, limit: int = 5) -> list[Submission]:
        return self.praw.subreddit(subreddit).new(limit=limit)
