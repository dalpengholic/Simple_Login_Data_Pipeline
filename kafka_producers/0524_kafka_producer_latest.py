from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext
from login_events import create_login_event
import os

# Define the Kafka topic
topic = 'mock_login_topic'
# Define the Kafka bootstrap servers and Schema Registry URL
bootstrap_servers = 'broker:9092'
schema_registry_url = 'http://schema-registry:8081'
# Create a Schema Registry client
schema_registry_conf = {'url': schema_registry_url}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)
# Define the Avro schema for the login event as a string
#with open(f"/app/avro/user_login.avsc") as f:
#    avro_schema_str = f.read() 

avro_value_schema_str = '''
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
# Define the Avro schema for the login event key
avro_key_schema_str = '''
{
  "type": "record",
  "name": "LoginEventKey",
  "fields": [
    {"name": "country", "type": "string", "default": "null"}
  ]
}
'''


# Create Avro serializers for the key and value
avro_key_serializer = AvroSerializer(schema_str=avro_key_schema_str, schema_registry_client=schema_registry_client)
avro_value_serializer = AvroSerializer(schema_str=avro_value_schema_str, schema_registry_client=schema_registry_client)

# Create a SerializationContext for value field
value_serialization_context = SerializationContext(
    topic=topic,
    field=MessageField.VALUE
)

# Create a SerializationContext for key field
key_serialization_context = SerializationContext(
    topic=topic,
    field=MessageField.KEY
)

# Create a Kafka producer instance
producer_conf = {
    'bootstrap.servers': bootstrap_servers
}
producer = Producer(producer_conf)

login_event_key, login_event_value = create_login_event()
# Serialize the key using the Avro serializer
serialized_key = avro_key_serializer(login_event_key, key_serialization_context)

# Serialize the value using the Avro serializer
serialized_value = avro_value_serializer(login_event_value, value_serialization_context)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))
# Produce the login event
producer.produce(topic=topic, key=serialized_key, value=serialized_value, callback=acked)
producer.poll(1)
