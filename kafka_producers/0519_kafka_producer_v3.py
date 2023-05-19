import random
import time
from datetime import datetime, timedelta
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define the Kafka topic to produce messages to
topic = 'yourtopic2'

# Define the list of possible browsers
browsers = ['safari', 'chrome', 'firefox', 'edge']

# Define the Kafka bootstrap servers
bootstrap_servers = 'broker:9092'

# Define the Schema Registry URL
schema_registry_url = 'http://schema-registry:8081'

# Define the Avro schema for the login event
login_event_schema = {
    "type": "record",
    "name": "LoginEvent",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "timestamp", "type": "string"},
        {"name": "browser_info", "type": "string"}
    ]
}

# Create a Kafka AvroProducer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'schema.registry.url': schema_registry_url
}

# Create an AvroProducer instance
producer = AvroProducer(producer_config, default_value_schema=login_event_schema)

# Generate and send mock login events
for i in range(1, 2000):
    # Generate a random timestamp within the range of 2022 Jan 1st and 2022 Dec 31st
    user_id = random.randint(1, 500)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    timestamp = random_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Select a random browser from the list
    browser = random.choice(browsers)

    # Create the login event
    login_event = {
        'user_id': f'user{user_id}',
        'timestamp': timestamp,
        'browser_info': browser
    }
    print(login_event, i)

    # Send the login event to the Kafka topic
    producer.produce(topic=topic, value=login_event)

    # Wait for the message to be delivered
    producer.flush()

    # Introduce a small delay between sending messages
    time.sleep(0.1)

# Flush and close the Kafka producer
producer.flush()
producer.close()

