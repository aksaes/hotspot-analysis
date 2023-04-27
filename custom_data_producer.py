# Some parts of the file may need to be modified to suit your environment
from confluent_kafka import Producer, Consumer, KafkaError

# set the topic name
topic_name = "test_data"
conf = {'bootstrap.servers': 'kafka-service:9092'} 

# create a Kafka producer instance
producer = Producer(conf)

# Check if the producer is connected to Kafka
print(producer.list_topics().topics)
print("-----------------------------")

message = 'Test message'

producer.produce(topic_name, value=message)
producer.flush()

# print
print("Message sent to Kafka: {}".format(message))


print(producer.list_topics().topics)
print("-----------------------------")

print('Consumer')

consumer_conf = {'bootstrap.servers': 'kafka-service:9092', 'group.id': 'mygroup', 'auto.offset.reset': 'earliest'}

consumer = Consumer(consumer_conf)
consumer.subscribe([topic_name])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'
                  .format(msg.topic(), msg.partition()))
        else:
            print('Error occured: {0}'.format(msg.error().str()))
    else:
        print('Received message: {0}'.format(msg.value()))
        break

consumer.close()