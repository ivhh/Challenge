from typing import List, Tuple
from datetime import datetime
from utils.pyspark_mng import PySparkManager
from utils.pyspark_schema import tweet_schema


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Reads a file containing JSON data and returns a list of tuples representing the date and username of the 10 users with the most tweets. (Time Performant)

    Args:
        file_path (str): The path to the file containing the JSON data.

    Returns:
        List[Tuple[datetime.date, str]]: A list of tuples, where each tuple contains the date (as a datetime.date object) and the username (as a string) of a user with the most tweets.
    """
    with PySparkManager() as spark:
        tweet_df = spark.read.json(file_path, schema=tweet_schema)
        top_tweets_df = (
            tweet_df.groupBy("date", "user.username")
            .count()
            .orderBy("count", ascending=False)
            .limit(10)
        )
        rows = top_tweets_df.collect()
        results = [(row["date"], row["username"]) for row in rows]
        return results
