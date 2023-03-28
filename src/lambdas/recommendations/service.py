import json

from common.threads.threads import call_with_threads
from lambdas.recommendations.wrappers.google_books_wrapper import GoogleBooksWrapper
from lambdas.recommendations.wrappers.open_ai_wrapper import AbstractOpenAIWrapper


def get_recommendations_from_text(
    open_ai_wrapper: AbstractOpenAIWrapper,
    google_books_wrapper: GoogleBooksWrapper,
    user_input: str,
) -> str:
    open_ai_response = open_ai_wrapper.query(
        messages=[
            {"role": "system", "content": "You are a book recommendation engine"},
            {
                "role": "user",
                "content": f"""
                Recommend a maximum of 20 books maximum meeting this criteria {user_input}.
                You can only respond in JSON with keys title t, author a.
                For example [{{ "t": title",  "a": "author"}}, {{ "t": title",  "a": "author"}}].""",
            },
        ]
    )
    open_ai_response_as_dict: list[dict] = json.loads(open_ai_response)

    google_books_responses = call_with_threads(
        function=google_books_wrapper.request_book,
        function_input=open_ai_response_as_dict,
    )
    google_books_responses = [
        response for response in google_books_responses if response
    ]

    return json.dumps([book.to_dict_by_alias() for book in google_books_responses])
