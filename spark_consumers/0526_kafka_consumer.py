from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, count, date_format
from pyspark.sql.types import StructType, StructField, StringType
from confluent_kafka import Consumer
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
import os

spark = SparkSession.builder.appName("KafkaToElasticsearch").getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Define the Kafka parameters
kafka_bootstrap_servers = "broker:9092"
kafka_topic = "mock_login_topic"
schema_registry_url = "http://schema-registry:8081"  

# Create a Schema Registry client
schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Define the Avro schema for the login event as a string
with open(f"/app/avro/user_login_key.avsc", 'r') as file_key, \
     open(f"/app/avro/user_login_value.avsc", 'r') as file_value:
    avro_key_schema_str = file_key.read()
    avro_value_schema_str = file_value.read()

# Create Avro serializers for the key and value
avro_key_deserializer = AvroDeserializer(schema_str=avro_key_schema_str, schema_registry_client=schema_registry_client)
avro_value_deserializer = AvroDeserializer(schema_str=avro_value_schema_str, schema_registry_client=schema_registry_client)

# Create a DeSerializationContext for value field
value_serialization_context = SerializationContext(
    topic=kafka_topic,
    field=MessageField.VALUE
)

# Create a DeSerializationContext for key field
key_serialization_context = SerializationContext(
    topic=kafka_topic,
    field=MessageField.KEY
)

# Create a Kafka producer instance
consumer_conf = {
    'bootstrap.servers': kafka_bootstrap_servers,
    "group.id": "spark-kafka-consumer",
    "auto.offset.reset": "earliest",
}
consumer = Consumer(consumer_conf)
consumer.subscribe([kafka_topic])

while True:
    try:
        # SIGINT can't be handled when polling, limit timeout to 1 second.
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        login_event_key = avro_key_deserializer(msg.key(), key_serialization_context)
        login_event_value = avro_value_deserializer(msg.value(), value_serialization_context)
        if login_event_key and login_event_value is not None:
            print("login_event_value record {}: user_id: {}\n"
                  "\ttimestamp: {}\n"
                  "\tbrowser_info: {}\n"
                  .format(login_event_key["country"], login_event_value["user_id"],
                          login_event_value["timestamp"],
                          login_event_value["browser_info"]))
    except KeyboardInterrupt:
        break

consumer.close()






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

