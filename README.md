# Simple Login Data Pipeline
Simple Login Data Pipeline consisting of 
data producer - message queue - data consumer


## 1st iteration 
### Project requirements
- Generally, a data pipeline for business user and/or data analyst consists of three sub-pipes. Data source or data producer, message queue and data consumer.
- For example, Let's assume that we are going to analyze user login data. any client apps and/or servers send each login event for anlayzing. The data are sent to almost a message queue app nowadays because it decouple the components of distributed system. Having a message queue makes a system scalable and resilient. For this project, Apache Kafka(Kafka) is already selected as a message queue app.
- When login events are stored in Kafka, the event will be gathered and aggregated to analyze user's behaviors. For instance, By collecting login event data with timestamps and grouping them by month, we can see the number of log-ins in a given month.

### Main goals
- Creating a working simple login data pipeline consisting of 3 components which are data producer, message queue(Kafka), and data consumer.
- ![diagram]()

### Risk assessment
- Apache Kafka(Kafka): No previous experience on Kafka and producer/consumer as well
  - Needing to study Kafka as well as get hands-on exprience by doing
- Data consumer: No idea which one is better between Apache Hadoop(Hadoop) or Apache Spark
- Programming language for this project
  - Kafka is wrtten in Scala, Java, Spark is written in Scala
  - It is known that making a Spark app using Scala or Java is better than using Python in terms of calculation speed

### Actions
- Kafka: 
  - Knowledge: Taking a short online course about Kafka to understand quickly 
  - Hands-on exprience: Istaliing and testing Kafka with console producer and consumer on localhost 
  - Packiging with docker after getting some knowledge and exprience
- Data producer: 
  - Creating a simple login mock data producer using Python and Kafka-producer client
- Data consumer:
  - After searching about Hadoop and Spark, I concluded that Spark will fit this project because I have dealt with Spark before and consumer should do an aggregation job and Spark could do this job well and faster than Hadoop. It is known that Spark can be 100x faster than Hadoop for smaller workloads via in-memory processing.
- Programming language:
  - I chose Python. At this stage, the main goal is to make a simple working datapipe line so that using Python that I am familiar with is better to learn another language. In the future, changing programming language can be considered.

### Results
- Decided tools as follows:
  - Data producer: `Kakfa-producer` client with Python
  - Message queue: `Apache Kafka` single node cluster
  - Data consumer: `Apache Spark` single node cluster. Spark Streaming used for Kafka consumer.
- All the tools written above are going to be run by docker-compose files on localhost
- ![result_screenshot]()



### Review
- There is a coupling kakfa-producer/kafka-spark-consumer script and docker container due to the fact running applications by docker. To enable a communication between containers correctly, container name of Kafka should be passed to kakfa-producer and kafka-spark-consumer script.
- After some docker build testing, using bitnami docker images for both kafka and spark is better than making my own image in terms of image size.
- Running Dockerized Kafka and Spark was straightforward, but it took me a while to integrate the Kafka producer and consumer with the Dockerized Kafka and Spark environment.

### How to run
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
[Persisting_your_data_from_bitnami](https://hub.docker.com/r/bitnami/kafka)
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
# Run below command when Kafka and Zookeeper settle down
docker-compose -f docker-compose.kafka-producer.yml up
# Run a single node Spark cluster
docker-compose -f docker-compose-spark-simple.yml up
# Run below command to get aggregated result of login data
docker exec -it spark-node bash -c 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 /0501_kafka_consumer.py'
```
