from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType
from graphframes import GraphFrame

spark = SparkSession.builder \
    .appName("CommunityDetection") \
    .config("spark.jars", "/Users/saimasharleen/PycharmProjects/pythonProject1/graphframes-0.8.1-spark3.0-s_2.12.jar") \
    .getOrCreate()

schema = StructType([
    StructField("user1", IntegerType(), True),
    StructField("user2", IntegerType(), True)
])

data = spark.read.csv("/Users/saimasharleen/PycharmProjects/pythonProject1/preprocessed_data.csv", schema=schema)

# Filter out rows with null values in user1 and user2 columns
data = data.filter("user1 IS NOT NULL AND user2 IS NOT NULL")

# Create a DataFrame with unique vertex IDs for users
users = data.select("user1").distinct().withColumnRenamed("user1", "id")

# Combine both user1 and user2 columns to create the edge DataFrame
edges = data.select("user1", "user2").withColumnRenamed("user1", "src").withColumnRenamed("user2", "dst")

# Create the GraphFrame using the vertex and edge DataFrames
G = GraphFrame(users, edges)

# Perform Label Propagation Algorithm (LPA) for community detection
result = G.labelPropagation(maxIter=5)

# Show the community assignments for each node
result.select("id", "label").show()
