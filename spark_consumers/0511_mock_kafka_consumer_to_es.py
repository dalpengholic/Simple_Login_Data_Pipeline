from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
from datetime import datetime

# create a SparkSession
spark = SparkSession.builder \
    .appName("PySpark to Elasticsearch example") \
    .config("es.nodes", "elasticsearch") \
    .config("es.port", "9200") \
    .getOrCreate()
data = [("Alicee", 21, datetime.now()), ("Bobb", 31, datetime.now()), ("Charliee", 36, datetime.now())]

# Define schema for DataFrame
schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("timestamp", TimestampType(), True)
])

# Create DataFrame from data and schema
df = spark.createDataFrame(data, schema=schema)

# Show DataFrame
df.show()


df.write.format("org.elasticsearch.spark.sql") \
    .option("es.resource", "myindex") \
    .mode("overwrite") \
    .save()

# stop the SparkSession
spark.stop()
