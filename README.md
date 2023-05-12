# Simple Login Data Pipeline
Simple Login Data Pipeline consisting of 
data producer - message queue - data consumer - data monitoring & visualization


## 2nd iteration 
### Project requirements
- A data pipeline having data source or data producer, message queue and data consumer was built after the 1st iteration.
- In this 2nd iteration, additiona sub pipeline is goint to be added at the end of data consumer sub pipeline so that any business decision makers or data analysts could take advantage of information presented using graphs and metrics

### Main goals
- Adding a working sub pipeline for data visualization and monitoring.
- ![diagram](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/simple-data-pipeline-drawio-2nd.png)

### Risk assessment
- Possible tools
  - Prometheus + Grafana: One of most popular visualization stack.
  - Elastic + Kibana: One of well known stack for search anddata visualization.
  - I decided to use Elastic + Kibana because I have experience of installation and managaing Elasticsearch and Kibana.
- Version selection of Elasticsearch and Kibana:
  - Having experience only version 8 having default SSL, which means a client of Elasticsearch should be configured correctly to communicate with Elasticsearch
  - It could be easy to install and run version 7 of Elasticsearch in terms of integration, but a new docker-compose file should be written
- Itegration with Spark and Elasticsearch: No previous experience on integration Spark as a Kafka consumer with Elasticsearch

### Actions
### Results
### How to run
```Shell
git clone https://github.com/dalpengholic/Simple_Login_Data_Pipeline.git
docker network create my-simple-network
cd Simple...
mkdir zookeeper_data kafka_data
sudo chown -R 1001:1001 zookeeper_data kafka_data 
docker-compose -f docker-compose.kafka.yml up -d
docker-compose -f docker-compose.kafka-producer.yml up -d
sudo sysctl -w vm.max_map_count=262144
mkdir es_data kibana_data 
sudo chown -R 1000:root es_data kibana_data
docker-compose -f docker-compose.es-kibana.yml up -d
docker cp es:/usr/share/elasticsearch/config/certs/ca/ca.crt .
sudo chown 1000:root ca.crt
mkdir spark_data_checkpoint
sudo chown 1001:root spark_data_checkpoint
docker-compose -f docker-compose-spark-simple.yml up -d
docker exec -it spark-node bash -c 'spark-submit --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.1.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /0501_kafka_consumer.py'
```
