import psycopg2

def create_table():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="my_database",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table with two columns (column1 and column2) to store the data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_table (
            sender TEXT,
            receiver TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()



# DATA (BATCH)

import pandas as pd

df = pd.read_csv("C:/Users/aless/Desktop/email-Eu-core.txt", sep = ' ', header=None, names = ['sender', 'receiver'])
# print(df)

# Convert pandas DataFrame to a list of tuples
data_tuples = df.to_records(index=False).tolist()



# INSERT DATA INTO TABLE

def insert_data(data_list):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="my_database",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Insert the data into the table
    for data in data_list:
        # Assuming data is a tuple with two elements (data for sender and receiver)
        cursor.execute('INSERT INTO data_table (sender, receiver) VALUES (%s, %s)', data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Data to be inserted into the database
data_to_insert = data_tuples

# Create the table (if it doesn't exist already)
create_table()

# Insert the data into the table
insert_data(data_to_insert)