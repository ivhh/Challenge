from typing import List, Tuple
from utils.operations import aggregate_multiline_json

from typing import List, Tuple


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Reads a file containing multiline JSON objects and aggregates the mentioned users. (Time Performant)

    Args:
        file_path (str): The path to the file containing the multiline JSON objects.

    Returns:
        List[Tuple[str, int]]: A list of tuples containing the mentioned user and the number of times they were mentioned.
    """
    return aggregate_multiline_json(
        file_path,
        ["mentionedUsers"],
        [("mentionedUsers", "str"), ("count", "int")],
        {"mentionedUsers": lambda x: [x["username"] for x in x]},
        "mentionedUsers",
    )
