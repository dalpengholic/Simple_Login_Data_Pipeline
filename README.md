# Simple Login Data Pipeline
Simple Login Data Pipeline consisting of 
data producer - message queue - data consumer - data monitoring & visualization

# README iteration
- [1st_README](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/README_1st_iteration.md)
- [2nd_README](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/README_2nd_iteration.md)

## 3rd iteration 
### Project requirements
- After 2nd iteration, the data pipeline was able to have data source or data producer, event queue, data consumer, and data analytic and monitoring layer by adding Elsticsearch, Kibana and Jupyter-Notebook with elasticsearch python client.
- In this 3rd iteration, this simple data pipeline has to become more advanced version by decoupling kafka-producer and application which calls kafka-producer wrapper and adding data schema management layer.

### Main goals
- Decoupling kafka-producer and application which calls kafka-producer wrapper
- Adding a schemy registry layer
- ![diagram](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/simple-data-pipeline-drawio-3rd.png)

### Risk assessment
- Making a kakfa-producer wrapper:
  - Expected difficulty level: easy
  - Real difficulty level: easy 

- Adding a schema registry layer
  - Expected difficulty level: easy
  - Real difficulty level: hard
    - Replacing Apache Kafka with Confluent Kafka
    - Replacing Kafka Python client with official Confluent Kafka Python client for both of producer and consumer
    - Adding a schema registry layer
    - Learning how to handle the framework of schema registry and kafka
    - Kafka message serialized by Confluent avro consists of 5 bytes(Schema id + magic byte) + Avro payload
    - Spark consumer should handle the 5 bytes correctly


### Actions
- Decoupling kafka-producer:
- Adding a schemm registry layer:
  - Replace bitnami/kafka with confluentinc/cp-server:7.3.0 image
  - Add and run confluentinc/cp-schema-registry:7.3.0 image
  - Edit Kafka producer app with Confluent Kafka Python client
  - Edit Spark consumer app with Confluent Kafka Python client and Submit with necessary pacakges
    - org.elasticsearch:elasticsearch-spark-30_2.12:8.1.2
    - org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0
    - org.apache.spark:spark-avro_2.12:3.4.0


### Results
- ![result1](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/es-captured-1.png)

- ![result2](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/es-captured-2.png)

### How to run
```Shell
git clone https://github.com/dalpengholic/Simple_Login_Data_Pipeline.git
docker network create my-simple-network
cd Simple...

# Set necessary folders
sudo sysctl -w vm.max_map_count=262144

# Run a single node cluster of zookeeper, kafka, and schema-registry
docker-compose -f docker-compose.schema-registry.yml up

# Run a Kafka producer 
docker-compose -f docker-compose.kafka-producer.yml up -d

# If you want to check Kafka from UI, run a UI for Kafka (After running below, access to localhost:8888 with a browser)
docker-compose -f docker-compose.ui-kafka.yml up -d

 
# Run a Elasticsearch and Kibana
mkdir es_data kibana_data spark_data spark_data_checkpoint
sudo chown -R 1001:1001 es_data kibana_data spark_data spark_data_checkpoint
docker-compose -f docker-compose.es-kibana.yml up -d

# Copying ca.crt
docker cp es:/usr/share/elasticsearch/config/certs/ca/ca.crt .
sudo chown 1001:1001 ca.crt

# Running a Spark cluseter
docker-compose -f docker-compose-spark-simple.yml up -d
docker exec -it spark-node bash -c 'spark-submit --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.1.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.spark:spark-avro_2.12:3.4.0 /0601_kafka_consumer.py'
```

### How to see graphs
```
# Open a broser at localhost:5601 (refer: .env)
- ID: elastic
- PASSWORD: 2KeW2V6tKyJaz9gu
```
- [Check_Kibana_README](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/README_kibana_dashboard.md) 


### Visualization layer added for Data Analyst
```Shell
docker-compose -f docker-compose.visual-layer.yml up
# Copy and paste or just click url from the console to open jupyter-notebook
# For instance) http://127.0.0.1:8888/?token=6624bb685c106f0cf89de947f409e34d98128b90fe4e4c9
```

