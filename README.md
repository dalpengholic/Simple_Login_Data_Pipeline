# Simple Login Data Pipeline
Simple Login Data Pipeline consisting of 
data producer - message queue - data consumer - data monitoring & visualization


## 3rd iteration 
### Project requirements
- After 2nd iteration, the data pipeline was able to have data source or data producer, event queue, data consumer, and data analytic and monitoring layer by adding Elsticsearch, Kibana and Jupyter-Notebook with elasticsearch python client.
- In this 3rd iteration, this simple data pipeline has to become more advanced version by decoupling kafka-producer and application which calls kafka-producer wrapper and adding data schema management layer.

### Main goals
- Decoupling kafka-producer and application which calls kafk
a-producer wrapper
- Adding a schemy registry layer
- ![diagram](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/simple-data-pipeline-drawio-2nd.png)

### Risk assessment
- Making a kakfa-producer wrapper:
  - Difficulty level: easy?
- Adding a schema registry layer
  - Difficulty levle: ??

### Actions
- Decoupling kafka-producer:
### Results
### How to run
```Shell
git clone https://github.com/dalpengholic/Simple_Login_Data_Pipeline.git
docker network create my-simple-network
cd Simple...

# Setting necessary folders
sudo sysctl -w vm.max_map_count=262144

# Running a single node cluster of zookeeper, kafka, and schema-registry
docker-compose -f docker-compose.schema-registry.yml up

# Running a Kafka producer 
docker-compose -f docker-compose.kafka-producer.yml up -d

# Running a Elasticsearch and Kibana
mkdir es_data kibana_data spark_data spark_data_checkpoint
sudo chown -R 1001:1001 es_data kibana_data spark_data spark_data_checkpoint
docker-compose -f docker-compose.es-kibana.yml up -d

# Copying ca.crt
docker cp es:/usr/share/elasticsearch/config/certs/ca/ca.crt .
sudo chown 1001:1001 ca.crt

# Running a Spark cluseter
docker-compose -f docker-compose-spark-simple.yml up -d
docker exec -it spark-node bash -c 'spark-submit --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.1.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /0519_kafka_consumer.py'
```

### Visualization layer added for Data Analyst
```Shell
docker-compose -f docker-compose.visual-layer.yml up
# Copy and paste or just click url from the console to open jupyter-notebook
# For instance) http://127.0.0.1:8888/?token=6624bb685c106f0cf89de947f409e34d98128b90fe4e4c9
```

