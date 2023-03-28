from concurrent.futures import ThreadPoolExecutor
from typing import Callable


def call_with_threads(function: Callable, function_input: list[any]):
    with ThreadPoolExecutor(max_workers=40) as executor:
        return executor.map(function, function_input)
