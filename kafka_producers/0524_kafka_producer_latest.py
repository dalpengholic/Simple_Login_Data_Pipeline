from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext
from login_events import create_login_event

# Define the Kafka topic
topic = 'mock_login_topic'
# Define the Kafka bootstrap servers and Schema Registry URL
bootstrap_servers = 'broker:9092'
schema_registry_url = 'http://schema-registry:8081'
# Create a Schema Registry client
schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
# Define the Avro schema for the login event as a string
avro_schema_str = '''
{
    "type": "record",
    "name": "LoginEvent",
    "fields": [
        {"name": "user_id", "type": "int"},
        {"name": "timestamp", "type": "string"},
        {"name": "browser_info", "type": "string"},
        {"name": "country", "type": "string", "default": "null"}   
    ]
}
'''

# Create an Avro serializer with the Schema Registry client and the Avro schema
avro_serializer = AvroSerializer(schema_str=avro_schema_str, schema_registry_client=schema_registry_client)

# Create a SerializationContext
serialization_context = SerializationContext(
        topic=topic,
        field=MessageField.VALUE  # Specify the field being serialized (in this case, the message value)
    )


# Create a Kafka producer instance
producer_conf = {
    'bootstrap.servers': bootstrap_servers
}
producer = Producer(producer_conf)

login_event = create_login_event()
serialized_login_event = avro_serializer(login_event, serialization_context) 

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))
# Produce the login event
producer.produce(topic=topic, key=None, value=serialized_login_event, callback=acked)
producer.poll(1)
