import psycopg2

try:
    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        database="my_database",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    print("Connection to PostgreSQL successful!")

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute an SQL query to view the content of the table
    try:
        table_name = 'data_table'
        query = f"SELECT * FROM {table_name};"
    
        cursor.execute(query)
        table_content = cursor.fetchall()

        # Display the content of the table
        for row in table_content:
            print(row)

    except psycopg2.Error as e:
        print(f"Error: {e}")

    # Close the connection
    conn.close()

except psycopg2.Error as e:
    print(f"Error: Could not connect to PostgreSQL: {e}")
