from typing import List, Tuple
from utils.pyspark_mng import PySparkManager
from utils.pyspark_schema import tweet_schema

from pyspark.sql.functions import explode

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Reads a file containing multiline JSON objects and aggregates the mentioned users. (Time Performant)

    Args:
        file_path (str): The path to the file containing the multiline JSON objects.

    Returns:
        List[Tuple[str, int]]: A list of tuples containing the mentioned user and the number of times they were mentioned.
    """
    with PySparkManager() as spark:
        tweet_df = spark.read.json(file_path, schema=tweet_schema)
        mentioned_users_df = tweet_df.select("mentionedUsers")
        # get only username in mentionedUsers
        # and then explode it to get each username in a row
        exploded_users_df = mentioned_users_df.withColumn(
            "mentionedUser", explode("mentionedUsers.username")
        )
        user_counts = (
            exploded_users_df.groupBy("mentionedUser")
            .count()
            .orderBy("count", ascending=False)
            .limit(10)
        )
        rows = user_counts.collect()
        results = [(row["mentionedUser"], row["count"]) for row in rows]
        return results
