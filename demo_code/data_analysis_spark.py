# data_analysis_spark.py
from pyspark.sql import SparkSession
import networkx as nx
import matplotlib.pyplot as plt

# Initialize a Spark session
spark = SparkSession.builder \
    .appName("DataAnalysisWithSpark") \
    .getOrCreate()


# Read data from PostgreSQL into a DataFrame
jdbc_url = "jdbc:postgresql://localhost:5432/saimasharleen"  # Replace with your actual values
properties = {
    "user": "postgres",          # Replace with your actual username
    "password": "postgres",      # Replace with your actual password
    "driver": "org.postgresql.Driver"
}
df = spark.read.jdbc(url=jdbc_url, table="demo", properties=properties)

# Perform some data filtering
df = df.filter((df.from_node_id < 100) & (df.to_node_id < 100))

# Convert DataFrame to Pandas DataFrame for further analysis with NetworkX
pandas_df = df.toPandas()

# Create a directed graph using NetworkX
G = nx.from_pandas_edgelist(pandas_df, source='from_node_id', target='to_node_id', create_using=nx.DiGraph())

# Perform degree centrality analysis
degree_centrality = nx.algorithms.centrality.degree_centrality(G)
sorted_degree_centrality = sorted(degree_centrality.items(), key=lambda item: item[1], reverse=True)
for i, (node, centrality) in enumerate(sorted_degree_centrality[:10]):
    print(f"Node: {node}, Degree Centrality: {centrality}")

# Perform other analyses using NetworkX as needed

# Visualization
plt.figure(figsize=(20, 20))
nx.draw_kamada_kawai(G, with_labels=True, node_size=300)
plt.title('Email, EU-Core network')
plt.show()

# Stop the Spark session
spark.stop()
