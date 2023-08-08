from pyspark.sql import SparkSession
from graphframes import GraphFrame
import psycopg2

def perform_graph_analysis(table_name):
    # Create a SparkSession
    spark = SparkSession.builder.appName("GraphAnalysis").getOrCreate()

    # Replace the connection details with your own
    conn = psycopg2.connect(
        database="saimasharleen",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Replace table_name with your actual table name
    query = f"SELECT FromNodeId, ToNodeId FROM data_table;"
    cur.execute(query)

    # Convert the data retrieved from PostgreSQL into a DataFrame
    data = [row for row in cur]
    df = spark.createDataFrame(data, schema=['src', 'dst'])

    # Create vertices DataFrame
    vertices_df = df.selectExpr("src as id").distinct()

    # Create a GraphFrame from the edges and vertices DataFrames
    graph = GraphFrame(vertices=vertices_df, edges=df)

    # Perform graph analysis using GraphFrame APIs
    # Example: Find the in-degree of each node
    in_degrees = graph.inDegrees

    # Show the results
    in_degrees.show()

    # Close the cursor and connection
    cur.close()
    conn.close()
