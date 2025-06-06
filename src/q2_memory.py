from typing import List, Tuple
from utils.emoji import get_emojis


from utils.operations import aggregate_multiline_json


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Calculates the frequency of emojis in a given file and returns a list of tuples
    containing the emoji and its count, sorted in descending order. (Memory Performant)

    Args:
        file_path (str): The path to the file containing the tweets.

    Returns:
        List[Tuple[str, int]]: A list of tuples containing the emoji and its count,
        sorted in descending order of count.
    """
    return aggregate_multiline_json(
        file_path,
        ["content"],
        [("content", "str"), ("count", "int")],
        {"content": get_emojis},
        "content",
    )
