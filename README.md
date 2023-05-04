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
![Persisting your data_from_bitnami](https://hub.docker.com/r/bitnami/kafka)
```Shell
sudo chown -R 1001:1001 zookeeper_data
sudo chown -R 1001:1001 kafka_data
```

4. Run with docker-compose
```Shell
docker-compose -f docker-compose.kafka.yml up
```
