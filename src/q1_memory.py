from typing import List, Tuple
from datetime import datetime
from typing import List

from utils.operations import aggregate_multiline_json

from typing import List, Tuple
import datetime


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Reads a file containing JSON data and returns a list of tuples representing the date and username of the 10 users with the most tweets. (Memory Performant)

    Args:
        file_path (str): The path to the file containing the JSON data.

    Returns:
        List[Tuple[datetime.date, str]]: A list of tuples, where each tuple contains the date (as a datetime.date object) and the username (as a string) of a user with the most tweets.
    """
    return aggregate_multiline_json(
        file_path,
        ["date", "user.username"],
        [("date", "date"), ("user.username", "str")],
        {"date": lambda x: x.split("T")[0]},
    )
