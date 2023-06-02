from pyspark.sql import SparkSession
from confluent_kafka.schema_registry import SchemaRegistryClient
import pyspark.sql.functions as fn
from pyspark.sql.avro.functions import from_avro


spark = SparkSession.builder.appName("KafkaToElasticsearch").getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Define the Kafka parameters
kafka_bootstrap_servers = "broker:9092"
kafka_topic = "mock_login_topic"
schema_registry_url = "http://schema-registry:8081"

# Create a Schema Registry client
schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

registered_value_schema = schema_registry_client.get_latest_version("mock_login_topic-value")
avro_value_schema_str = registered_value_schema.schema.schema_str
print(avro_value_schema_str)

# Read stream
df = spark.read.format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "earliest") \
    .load() 
#    .selectExpr("substring(value, 6, length(value)-5) as avro_value") \
#    .select(from_avro(fn.col("avro_value"), avro_value_schema_str).alias("data")).select("data.*")

df.printSchema()

df1 = df.withColumn('fixedValue', fn.expr("substring(value, 6, length(value)-5)")) \
        .select(from_avro(fn.col("fixedValue"), avro_value_schema_str).alias("data")).select("data.*")

df1.printSchema()
#df1.show(2)

# Convert timestamp to date and extract month
df1 = df1.withColumn("datetype_timestamp", fn.to_timestamp(fn.col("timestamp")))
df1.printSchema()
#df1.show(2)

# Convert timestamp to date and extract month
df1 = df1.withColumn("date", df1.datetype_timestamp.cast("date"))
df1 = df1.withColumn("month", fn.date_format("date", "yyyy-MM"))
df1.printSchema()
df1.show(2)

