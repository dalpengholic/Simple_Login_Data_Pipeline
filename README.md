# Simple Login Data Pipeline
Simple Login Data Pipeline consisting of 
data producer - message queue - data consumer - data monitoring & visualization


## 2nd iteration 
### Project requirements
- A data pipeline having data source or data producer, event queue and data consumer was built after the 1st iteration.
- In this 2nd iteration, additional sub pipeline is added at the end of data consumer sub pipeline so that any business decision makers or data analysts could take advantage of information presented using graphs and metrics

### Main goals
- Adding a working sub pipeline for data visualization and monitoring.
- ![diagram](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/simple-data-pipeline-drawio-2nd.png)

### Risk assessment
- Possible tools
  - Prometheus + Grafana: One of most popular visualization stack. Less experience of installation and operation.
  - Elasticsearch + Kibana: One of well known stack for search and data visualization.
  - Elasticsearch + Kibana stack is selected to reduce additional learning time and focus on adding visulaization function to the whole pipeline.
- Version selection of Elasticsearch and Kibana:
  - Having experience only version 8 having default SSL, which means a client of Elasticsearch should be configured correctly to communicate with Elasticsearch.
  - From integration point of view, installation and operation of version 7 of Elasticsearch could be easy due to the fact of no authentication needed, but a new docker-compose file should be written.
  - Version 8 of Elasticsearch and Kibana is chosen. However, the cost of SSL configuration between spark and Elasticsearch should be payed.
- Integration with Spark and Elasticsearch: No previous experience on integration Spark as a Kafka consumer with Elasticsearch

### Actions
- Elasticsearch and Kibana:
  - Use a ready-made docker-compose.yml file made by myself and modify it to have docker-compose-es-spark-integration.yml which runs Spark and Elasticsearch and Kibana together. 
  - For getting proper configuration, creating a simple dataframe at Spark and push it to Elasticsearch by using 0511_mock_kafka_consumer_to_es.py under spark_consumers folder.
  - After confirming a correct integration between Spark and Elasticsearch, updating the real consumer file `0501_kafka_consumer.py` to push data from Spark Streaming to Elasticsearch.
### Results
- Decided tools as follows:
  - At the 1st iteration
    - Data producer: `Kakfa-producer` client with Python
    - Event queue: `Apache Kafka` single node cluster
    - Data consumer: `Apache Spark` single node cluster. Spark Streaming used for Kafka consumer.
  - At the 2nd iteration
    - Data visualiation layer: 
      - `Elasticsearch` to store the aggregated data from Saprk
      - `Kibana` to draw graphs and show metrics
- All the tools written above could be run by docker-compose files on localhost
- The below is the result of show a near real time metrics and graphs. The aggregated user login information is pushed to Elasticsearch by Spark Streaming and Kibana keep refreshing evert 1 second so that it could present update login infomration. 
- ![result_screenshot](https://github.com/dalpengholic/Simple_Login_Data_Pipeline/blob/master/pics/Screenshot-ES.png)



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
sudo chown -R 1001:root es_data kibana_data
docker-compose -f docker-compose.es-kibana.yml up -d
docker cp es:/usr/share/elasticsearch/config/certs/ca/ca.crt .
sudo chown 1001:root ca.crt
mkdir spark_data_checkpoint
sudo chown 1001:root spark_data_checkpoint
docker-compose -f docker-compose-spark-simple.yml up -d
docker exec -it spark-node bash -c 'spark-submit --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.1.2,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /0501_kafka_consumer.py'
```
