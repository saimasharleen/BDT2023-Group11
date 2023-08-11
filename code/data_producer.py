from kafka import KafkaProducer

# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Read data from the file and send it to Kafka
with open('/Users/saimasharleen/PycharmProjects/finalproject/email-EuAll.txt', 'r') as file:
    for line in file:
        producer.send('email-data-topic', value=line.strip().encode('utf-8'))

# Close the producer
producer.close()
