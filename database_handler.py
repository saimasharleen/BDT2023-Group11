import psycopg2
import pandas as pd

def create_table_if_not_exists(table_name, data):
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            database="saimasharleen",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Check if the table already exists
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');"
        cursor.execute(query)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            # Create the table with appropriate data types based on DataFrame columns
            # Here we assume the columns 'FromNodeId' and 'ToNodeId' are integers.
            # If they are different data types, adjust the data types accordingly.
            create_query = f"CREATE TABLE {table_name} (FromNodeId INT, ToNodeId INT);"
            cursor.execute(create_query)
            print(f"Table {table_name} created successfully!")

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error: {e}")

def store_data_in_database(data, table_name):
    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            database="saimasharleen",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print("Connection to PostgreSQL successful!")

        # Create the table if it does not exist
        create_table_if_not_exists(table_name, data)

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Assuming the data DataFrame has columns 'FromNodeId' and 'ToNodeId'
        for index, row in data.iterrows():
            # Convert 'numpy.int64' to Python 'int'
            from_node_id = int(row['FromNodeId'])
            to_node_id = int(row['ToNodeId'])

            # Use the correct column names in the INSERT INTO query
            query = f"INSERT INTO {table_name} (FromNodeId, ToNodeId) VALUES (%s, %s);"
            cursor.execute(query, (from_node_id, to_node_id))

        # Commit the changes
        conn.commit()
        print("Data inserted successfully!")

    except psycopg2.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

# Read data from CSV file (assuming you already have this step)
data = pd.read_csv('/Users/saimasharleen/PycharmProjects/pythonProject1/email-EuAll.txt', sep='\t')

# Replace 'data_table' with your actual table name
store_data_in_database(data, table_name='data_table')
