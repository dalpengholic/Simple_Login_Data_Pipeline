from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer, AvroDeserializer
from confluent_kafka.serialization import SerializationContext
from login_events_generator import create_login_event
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
with open(f"/app/avro/user_login_key.avsc", 'r') as file_key, \
     open(f"/app/avro/user_login_value.avsc", 'r') as file_value:
    avro_key_schema_str = file_key.read()
    avro_value_schema_str = file_value.read()


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
        avro_deserializer = AvroDeserializer(schema_str=avro_value_schema_str, schema_registry_client=schema_registry_client)
        ori_login_event = avro_deserializer(msg.value(), value_serialization_context)
        print(ori_login_event)
        print("Message produced: %s" % (str(msg.value())))


def generate_and_send_login_events(num_events, producer, callback):
    for _ in range(num_events):
        login_event_key, login_event_value = create_login_event()
        
        # Serialize the key using the Avro serializer
        serialized_key = avro_key_serializer(login_event_key, key_serialization_context)
        
        # Serialize the value using the Avro serializer
        serialized_value = avro_value_serializer(login_event_value, value_serialization_context)
        
        # Produce the login event
        producer.produce(topic=topic, key=serialized_key, value=serialized_value, callback=callback)
        producer.poll(1)

# Generate and send multiple login events
generate_and_send_login_events(2000, producer, acked)

# Wait for any outstanding messages to be delivered and delivery report callbacks to be triggered
producer.flush()


# Produce the login event
#producer.produce(topic=topic, key=serialized_key, value=serialized_value, callback=acked)
#producer.poll(1)
