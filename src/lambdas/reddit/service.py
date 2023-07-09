from common.wrappers.recommendation_wrapper import RecommendationAIWrapper
from common.wrappers.reddit_wrapper import RedditWrapper

CLIENT_ID = "drb9MFYRHyf9Tv2IqekbUg"
SECRET = "CaqwwEG8sAO7xKIqdSPJ-7kyoR8Jtw"


def make_reddit_responses(
    reddit_wrapper: RedditWrapper, recommendation_wrapper: RecommendationAIWrapper
):
    posts = reddit_wrapper.get_new_posts(subreddit="suggestmeabook")

    # TODO (ZF) - Batch get posts so that we can identify which have already been replied to
    posts = [post for post in posts]  # exhaust generator
    post_ids = [post.id for post in posts]  # exhaust generator
    print(post_ids)

    for post in posts:
        summarised_post = recommendation_wrapper.summarise_user_input(
            title=post.title, body=post.selftext
        )
        print(summarised_post)
        recommendations = recommendation_wrapper.get_book_recommendations_from_text(
            user_input=summarised_post, recommendation_count=5
        )
        print(recommendations)
        print("---")


if __name__ == "__main__":
    reddit_wrapper = RedditWrapper(
        client_id=CLIENT_ID,
        client_secret=SECRET,
        user_agent="PagePunditBot",
        username="test",
        password="user",
    )
    make_reddit_responses(
        reddit_wrapper=reddit_wrapper,
        recommendation_wrapper=RecommendationAIWrapper(
            api_key="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"
        ),
    )
