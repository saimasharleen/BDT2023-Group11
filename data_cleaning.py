from kafka import KafkaConsumer
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='your_database_name',
    user='your_username',
    password='your_password',
    host='your_host'
)

# Create a cursor
cur = conn.cursor()

# Create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS email_data (
    id SERIAL PRIMARY KEY,
    from_node_id INT,
    to_node_id INT
)
'''

cur.execute(create_table_query)

# Create a Kafka consumer
consumer = KafkaConsumer('email-data-topic', bootstrap_servers='localhost:9092')

# Clean and insert data
for msg in consumer:
    data = msg.value.decode('utf-8').split('\t')
    if len(data) == 2:
        from_node_id, to_node_id = int(data[0]), int(data[1])
        insert_query = '''
        INSERT INTO email_data (from_node_id, to_node_id)
        VALUES (%s, %s)
        '''
        cur.execute(insert_query, (from_node_id, to_node_id))
        conn.commit()

# Close consumer, cursor, and connection
consumer.close()
cur.close()
conn.close()
