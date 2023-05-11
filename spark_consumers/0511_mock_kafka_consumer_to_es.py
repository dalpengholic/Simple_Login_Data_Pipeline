from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder \
    .appName("Push DataFrame to Elasticsearch") \
    .config("spark.es.nodes", "es") \
    .config("spark.es.port", "9200") \
    .config("spark.es.nodes.wan.only", "true") \
    .config("spark.es.net.ssl", "true") \
    .config("spark.es.net.ssl.cert.allow.self.signed", "true") \
    .config("spark.es.net.ssl.cert.ca", "ca.crt") \
    .config("spark.es.net.http.auth.user", "elastic") \
    .config("spark.es.net.http.auth.pass", "2KeW2V6tKyJaz9gu") \
    .config("spark.es.nodes.wan.only", "true") \
    .getOrCreate()


# Define the Elasticsearch index and document type
es_index = "my_index"
es_doc_type = "my_doc_type"

# Create a sample DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35),("Deen", 15),("Flora",19)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()

# Write the DataFrame to Elasticsearch
df.write \
    .format("org.elasticsearch.spark.sql") \
    .option("es.resource", es_index) \
    .mode("overwrite") \
    .save()

# Stop the Spark session
spark.stop()

