
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType
from pyspark.sql.types import StringType
from pyspark.sql.functions import col, from_json, lit, date_format, count
 
spark = SparkSession.builder.appName("KafkaToElasticsearch").getOrCreate()
 
spark.sparkContext.setLogLevel('ERROR')
 
# Define the Kafka parameters
kafka_bootstrap_servers = "kafka:9092"
kafka_topic = "yourtopic2"
 
# Read stream
df = spark.readStream.format("kafka") \
.option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
.option("subscribe", kafka_topic) \
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
#result = result.orderBy(col("total_logins").desc())


# Write result to temporary table
# result.createOrReplaceTempView("temp_table")

# Query the temporary table to retrieve sorted result by month
# sorted_result = spark.sql("SELECT * FROM temp_table ORDER BY month ASC")

# Define the Elasticsearch parameters
es_host = "es"
es_port = "9200"
es_index = "user-login"
es_user = "elastic"
es_pass = "2KeW2V6tKyJaz9gu"


# Write the DataFrame to Elasticsearch
result.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", es_host) \
    .option("es.port", es_port) \
    .option("es.nodes.wan.only", "true") \
    .option("es.net.ssl", "true") \
    .option("es.net.ssl.cert.allow.self.signed", "true") \
    .option("es.net.ssl.cert.ca", "ca.crt") \
    .option("es.net.http.auth.user", es_user) \
    .option("es.net.http.auth.pass", es_pass) \
    .option("es.nodes.wan.only", "true") \
    .option("es.resource", es_index) \
    .option("checkpointLocation", "/checkpoint") \
    .option("es.mapping.id", "month") \
    .option("es.index.auto.create", "true") \
    .outputMode("Update") \
    .start() \
    .awaitTermination()


# Wait for the query to finish
#query.awaitTermination()


