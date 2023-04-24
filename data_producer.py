from confluent_kafka import Producer
import pyarrow.parquet as pq
import time
import pandas as pd

# set the topic name
topic_name = "nyc_taxicab_data"
conf = {'bootstrap.servers': 'localhost:30092'}

# create a Kafka producer instance
producer = Producer(conf)

# Check if the producer is connected to Kafka
print(producer.list_topics().topics)
print("-----------------------------")

# load the Parquet dataset
trips = pq.read_table('yellow_tripdata_2022-03.parquet')
trips = trips.to_pandas()

# iterate over each row in the table and send it to Kafka
for index, row in trips.iterrows():
    # encode the row as bytes
    message = str(row).encode('utf-8')

    # send the message to Kafka
    producer.produce(topic_name, value=message)

    # print
    print("Message sent to Kafka: {}".format(message))

    # wait for 0.1 seconds
    time.sleep(0.1)

# close the producer connection
producer.close()
