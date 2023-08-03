import pandas as pd
import networkx as nx
import community
import matplotlib.pyplot as plt

# Load the dataset (replace 'path_to_dataset' with the actual path)
data = pd.read_csv("/Users/saimasharleen/PycharmProjects/pythonProject1/facebook_combined.txt", sep=' ', header=None, names=['user1', 'user2'])

# Create an empty undirected graph
G = nx.Graph()

# Add edges from the dataset to the graph
for row in data.itertuples(index=False):
    G.add_edge(row.user1, row.user2)

# Perform Louvain community detection
partition = community.best_partition(G)

# Create a DataFrame to store the community assignment for each node
community_df = pd.DataFrame(partition.items(), columns=['node', 'community'])

# Calculate the clustering coefficient for each node
clustering_coefficients = nx.clustering(G)

# Add clustering coefficient as an attribute to each node in the graph
nx.set_node_attributes(G, clustering_coefficients, name='clustering_coefficient')

# Get the number of communities and the nodes belonging to each community
num_communities = max(partition.values()) + 1
communities = {}
for node, community_id in partition.items():
    if community_id not in communities:
        communities[community_id] = []
    communities[community_id].append(node)

# Display the clustering coefficient for each node and its community
for community_id, nodes in communities.items():
    print(f"Community {community_id}: {nodes}")
    for node in nodes:
        clustering_coefficient = G.nodes[node]['clustering_coefficient']
        print(f"Node {node}: Clustering Coefficient = {clustering_coefficient}")

    print("\n")
