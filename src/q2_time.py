from typing import List, Tuple
from utils.pyspark_mng import PySparkManager
from utils.pyspark_schema import tweet_schema

from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import explode
from utils.emoji import get_emojis

# Convert the get_emojis function to an UDF
get_emojis_udf = udf(get_emojis, ArrayType(StringType()))


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Calculates the frequency of emojis in a given file and returns a list of tuples
    containing the emoji and its count, sorted in descending order. (Time Performant)

    Args:
        file_path (str): The path to the file containing the tweets.

    Returns:
        List[Tuple[str, int]]: A list of tuples containing the emoji and its count,
        sorted in descending order of count.
    """
    with PySparkManager() as spark:
        content_df = spark.read.json(file_path, schema=tweet_schema).select("content")
        emojis_df = content_df.withColumn("emojis", get_emojis_udf(content_df["content"]))
        exploded_emojis_df = emojis_df.select("emojis").withColumn(
            "emoji", explode("emojis")
        )
        emoji_counts = (
            exploded_emojis_df.groupBy("emoji")
            .count()
            .orderBy("count", ascending=False)
            .limit(10)
        )
        rows = emoji_counts.collect()
        results = [(row["emoji"], row["count"]) for row in rows]
        return results
