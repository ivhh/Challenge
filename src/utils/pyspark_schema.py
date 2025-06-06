from pyspark.sql.types import (
    StructType,
    StructField,
    LongType,
    DateType,
    StringType,
    ArrayType,
    IntegerType
)

user_schema = StructType(
    [
        StructField("id", LongType(), False),
        StructField("username", StringType(), False),
    ]
)
"""user_schema: Base Schema for the user data"""

tweet_schema = StructType(
    [
        StructField("id", LongType(), False),
        StructField("date", DateType(), False),
        StructField("content", StringType(), False),
        StructField("user", user_schema, False),
        StructField("retweetCount", IntegerType(), True),
        StructField("mentionedUsers", ArrayType(user_schema), True),
    ]
)
"""tweet_schema: Base Schema for the tweet data"""
