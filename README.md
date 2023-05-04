# Simple_Login_Data_Pipeline
Simple_Login_Data_Pipeline consisting of data producer - message queue - data consumer

## Main Goals
## Requirements
## How to run
1. Clone this repo to your local host
```Shell
git clone https://github.com/dalpengholic/Simple_Login_Data_Pipeline.git
```

2. Create two directories for Kafka and Zookeeper at current cloned path
```Shell
mkdir kafka_data
mkdir zookeeper_data
```

3. Change ownership of those two directory
[Persisting your data_from_bitnami](https://hub.docker.com/r/bitnami/kafka)
```Shell
sudo chown -R 1001:1001 zookeeper_data
sudo chown -R 1001:1001 kafka_data
```

4. Create a user-defined network 
```Shell
docker network create my-simple-network
```

5. Run with docker-compose
```Shell
docker-compose -f docker-compose.kafka.yml up
# Run below command when kafka and zookeeper settle down
docker-compose -f docker-compose.kafka-producer.yml up
docker-compose -f docker-compose-spark-simple.yml up
# Run below command to get aggregated result of login data
docker exec -it spark-node bash -c 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /0501_kafka_consumer.py'
```
