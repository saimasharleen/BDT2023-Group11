import sqlite3
import pandas as pd

def read_data_from_database():
    # Connect to the database
    conn = sqlite3.connect('data.db')

    # Read data from the database using SQL query
    query = 'SELECT * FROM data_table'
    data_df = pd.read_sql_query(query, conn)

    # Close the connection
    conn.close()

    return data_df

# Call the function to retrieve data from the database and create a pandas DataFrame
df = read_data_from_database()

# Display the retrieved data
# print(df)

import networkx as nx

# Assuming the df has columns "sender" and "receiver"

import pandas as pd

def create_social_graph(logs_df):
    G = nx.DiGraph()
    for _, row in logs_df.iterrows():
        sender = row["sender"]
        receiver = row["receiver"]
        G.add_edge(sender, receiver)
    return G

G = create_social_graph(df)

def basic_network_analysis(G):
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Degree Distribution: {dict(G.degree())}")
    print(f"Clustering Coefficient: {nx.average_clustering(G)}")
    print(f"Density: {nx.density(G)}")
    print(f"Centralization: {nx.degree_centrality(G)}")


basic_network_analysis(G)


def community_detection(G):
    communities = nx.community.girvan_newman(G)
    top_level_communities = next(communities)
    print(f"Communities: {list(top_level_communities)}")

community_detection(G)


