import random
import time
from datetime import datetime, timedelta
from confluent_kafka import Producer
import json

# Define the Kafka topic to produce messages to
topic = 'yourtopic2'

# Define the list of possible browsers
browsers = ['safari', 'chrome', 'firefox', 'edge']

# Define the Kafka bootstrap servers
bootstrap_servers = 'localhost:9092'

# Create a Kafka producer configuration
producer_config = {'bootstrap.servers': bootstrap_servers}

# Create a Kafka producer instance
producer = Producer(producer_config)

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

    # Create the login event JSON object
    login_event = {
        'user_id': f'user{user_id}',
        'timestamp': timestamp,
        'browser_info': browser
    }
    print(login_event, i)

    # Convert the login event to JSON format
    login_event_json = json.dumps(login_event)

    # Send the login event to the Kafka topic
    producer.produce(topic, value=login_event_json.encode('utf-8'))

    # Wait for the message to be delivered
    producer.flush()

    # Introduce a small delay between sending messages
    time.sleep(0.1)

# Flush and close the Kafka producer
producer.flush()
producer.close()

