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
- Version of Elasticsearch and Kibana: No previous experience on Kafka and producer/consumer as well
- Itegration with Spark and Elasticsearch

### Actions
### Results
### How to run
1. Clone this repo to your local host
```Shell
```

2. Create two directories for Kafka and Zookeeper at current cloned path
```Shell
```

3. Change ownership of those two directory
```Shell
```

4. Create a user-defined network 
```Shell
```

5. Run with docker-compose
```Shell
```
