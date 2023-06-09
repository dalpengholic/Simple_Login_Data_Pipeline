from pyspark.sql import SparkSession
from pyspark.sql.functions import  col, from_json, count, date_format
from pyspark.sql.types import StructType, StructField, StringType

spark = SparkSession.builder.appName("KafkaToElasticsearch").getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Define the Kafka parameters
kafka_bootstrap_servers = "broker:9092"
kafka_topic = "mock_login_topic"
schema_registry_url = "http://schema-registry:8081"  

# Read stream
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .load()

df.printSchema()

# Define the Avro schema for the login event
avro_schema = StructType([
    StructField("user_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("browser_info", StringType())
])


# Apply Avro deserialization to the value column
df = df.select(from_json(col("value").cast("string"), avro_schema).alias("data")).select("data.*")


# Convert timestamp to date and extract month
df = df.withColumn("date", df.timestamp.cast("date"))
df = df.withColumn("month", date_format("date", "yyyy-MM"))

# Group by user_id and month, and count the logins
result = df.groupBy("month").agg(count("*").alias("total_logins"))
# Sort the result in descending order based on total_logins
#result = result.orderBy(col("total_logins").desc())

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

