from pyspark.sql import SparkSession


class PySparkManager:
    """
    Singleton class to manage PySpark session
    """

    _instance = None
    _app_name = "LATAM-DE"
    _spark: SparkSession

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __enter__(cls):
        cls._start()
        return cls._spark

    def __exit__(cls, exc_type, exc_val, exc_tb):
        pass

    def _start(cls):
        cls._spark = SparkSession.builder.appName(cls._app_name).getOrCreate()

    def _stop(cls):
        return cls._spark.stop()
