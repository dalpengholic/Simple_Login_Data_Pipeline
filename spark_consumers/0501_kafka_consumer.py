
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType
from pyspark.sql.types import StringType
from pyspark.sql.functions import col, from_json, lit, date_format, count
 
spark = SparkSession.builder.config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0").getOrCreate()
 
spark.sparkContext.setLogLevel('ERROR')
 
# Read stream
df = spark.readStream.format("kafka") \
.option("kafka.bootstrap.servers", "kafka:9092") \
.option("subscribe", "yourtopic2") \
.option("startingOffsets", "earliest") \
.load()

df.printSchema() 

kafka_df = df.selectExpr("CAST(value AS STRING)")

schema = StructType([
    StructField("user_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("browser_info", StringType()),
])

schema_json = schema.json()
# Apply schema to the JSON data
kafka_df = kafka_df.select(from_json(col("value"), schema).alias("data")).select("data.*")


# Convert timestamp to date and extract month
kafka_df = kafka_df.withColumn("date", kafka_df.timestamp.cast("date"))
kafka_df = kafka_df.withColumn("month", date_format("date", "yyyy-MM"))

# Group by user_id and month, and count the logins
result = kafka_df.groupBy("month").agg(count("*").alias("total_logins"))
# Sort the result in descending order based on total_logins
result = result.orderBy(col("total_logins").desc())


# Write result to temporary table
result.createOrReplaceTempView("temp_table")

# Query the temporary table to retrieve sorted result by month
sorted_result = spark.sql("SELECT * FROM temp_table ORDER BY month ASC")

# Write data to console
query = sorted_result \
    .writeStream \
    .format("console") \
    .outputMode("complete") \
    .start()

# Wait for the query to finish
query.awaitTermination()


