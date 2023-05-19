import random
import time
from datetime import datetime, timedelta
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define the Kafka topic to produce messages to
topic = 'yourtopic2'

# Define the list of possible browsers
browsers = ['safari', 'chrome', 'firefox', 'edge']

# Define the Kafka bootstrap servers and Schema Registry URL
bootstrap_servers = 'broker:9092'
schema_registry_url = 'http://schema-registry:8081'  # Replace with your Schema Registry URL

# Create an AvroProducer configuration
producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'schema.registry.url': schema_registry_url
}

# Create an AvroProducer instance
producer = AvroProducer(producer_config)

# Define the Avro schema for the login event
login_event_schema_str = '''
{
    "type": "record",
    "name": "LoginEvent",
    "fields": [
        {"name": "user_id", "type": "string"},
        {"name": "timestamp", "type": "string"},
        {"name": "browser_info", "type": "string"}
    ]
}
'''

# Parse the Avro schema
login_event_schema = avro.loads(login_event_schema_str)

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

    # Create the login event record
    login_event = {
        'user_id': f'user{user_id}',
        'timestamp': timestamp,
        'browser_info': browser
    }
    print(login_event, i)


    # Produce the login event using Avro serialization
    producer.produce(
        topic=topic,
        value=login_event,
        value_schema=login_event_schema
    )

    # Wait for the message to be delivered
    producer.flush()

    # Introduce a small delay between sending messages
    time.sleep(0.1)

# Flush and close the Kafka producer
producer.flush()
producer.close()

