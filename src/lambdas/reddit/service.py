import logging

from praw.reddit import Reddit

import common.logic.recommendation as shared_logic
from common.model.book import BookRecommendationResponse
from common.repository.recommendation import DynamoRecommendationRepo
from common.wrappers.google_books_wrapper import GoogleBooksWrapper
from common.wrappers.recommendation_wrapper import RecommendationAIWrapper

logging.basicConfig(level=logging.INFO)


def convert_to_markdown_post(recommendation: BookRecommendationResponse) -> str:
    post_content = [
        'I am the PagePundit Bot. I use AI to provide recommendations based on your post.',
        f'Here are {len(recommendation.books)} books I think will be of interest!'
    ]
    for i, book in enumerate(recommendation.books):
        book_link = f"[{book.title}](https://pagepundit.com/#/recommendation/{recommendation.recommendation_id}/{i})"
        if book.authors:
            book_link += f" - By {', '.join(book.authors)}"
        post_content.append(book_link)
    return "\n\n".join(post_content)


def make_reddit_responses(
    reddit_wrapper: Reddit,
    recommendation_wrapper: RecommendationAIWrapper,
    recommendation_repo: DynamoRecommendationRepo,
    google_books_wrapper: GoogleBooksWrapper,
) -> None:
    posts = reddit_wrapper.subreddit('recommendmeabook').new(limit=50)

    for post in posts:
        has_already_replied = any(top_level_comment.author == 'PagePundit' and top_level_comment.body.startswith('I am the PagePundit Bot.') for top_level_comment in post.comments)
        if has_already_replied:
            logging.info(f'Skipping post {post.id} as already replied')
            continue

        summarised_post = recommendation_wrapper.summarise_user_input(
            title=post.title, body=post.selftext
        )
        new_recommendations = shared_logic.get_and_store_recommendations_from_text(
            user_input=summarised_post,
            recommendation_repo=recommendation_repo,
            google_books_wrapper=google_books_wrapper,
            recommendation_wrapper=recommendation_wrapper,
            recommendation_limit=6,
        )
        response = convert_to_markdown_post(recommendation=new_recommendations)
        submission = reddit_wrapper.submission(id=post.id)
        submission.reply(response)
        logging.info(f'Posted new recommendations for post {post.id}')
