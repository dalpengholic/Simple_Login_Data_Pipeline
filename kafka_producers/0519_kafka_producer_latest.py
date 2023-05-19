import random
import time
from datetime import datetime, timedelta
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

class KafkaProducer:
    def __init__(self, bootstrap_servers, schema_registry_url, topic, schema_str):
        self.bootstrap_servers = bootstrap_servers
        self.schema_registry_url = schema_registry_url
        self.topic = topic
        self.schema_str = schema_str
        self.producer = None
        self.schema = None

    def initialize(self):
        # Create an AvroProducer configuration
        producer_config = {
            'bootstrap.servers': self.bootstrap_servers,
            'schema.registry.url': self.schema_registry_url
        }

        # Create an AvroProducer instance
        self.producer = AvroProducer(producer_config)

        # Parse the Avro schema
        self.schema = avro.loads(self.schema_str)

    def produce_login_events(self, num_events, browsers):
        for i in range(1, num_events + 1):
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
            self.producer.produce(
                topic=self.topic,
                value=login_event,
                value_schema=self.schema
            )

            # Wait for the message to be delivered
            self.producer.flush()

            # Introduce a small delay between sending messages
            time.sleep(0.1)

    def close(self):
        # Flush and close the Kafka producer
        self.producer.flush()

# Define the Kafka topic to produce messages to
topic = 'yourtopic2'

# Define the list of possible browsers
browsers = ['safari', 'chrome', 'firefox', 'edge']

# Define the Kafka bootstrap servers and Schema Registry URL
bootstrap_servers = 'broker:9092'
schema_registry_url = 'http://schema-registry:8081'  

# Define the Avro schema for the login event as a string
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

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers, schema_registry_url, topic, login_event_schema_str)

# Initialize the producer
producer.initialize()

# Generate and send mock login events
producer.produce_login_events(2000, browsers)

# Close the Kafka producer
producer.close()

