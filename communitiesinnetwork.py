import pandas as pd
import networkx as nx
import community  # This is the Louvain community detection library for NetworkX

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

# Display the community assignment for each node
print(community_df)

# Get the number of communities and the nodes belonging to each community
num_communities = max(partition.values()) + 1
communities = {}
for node, community_id in partition.items():
    if community_id not in communities:
        communities[community_id] = []
    communities[community_id].append(node)

# Display the nodes belonging to each community
for community_id, nodes in communities.items():
    print(f"Community {community_id}: {nodes}")

# Modularity Calculation
modularity = community.modularity(partition, G)
print("Modularity:", modularity)

# Average Degree Calculation
def average_degree(graph, community):
    total_degree = sum(dict(graph.degree(community)).values())
    return total_degree / len(community)
for idx, community_nodes in communities.items():
    avg_degree = average_degree(G, community_nodes)
    print(f"Community {idx} - Average Degree:", avg_degree)

# Density Calculation
def density(graph, community):
    subgraph = graph.subgraph(community)
    num_edges_within_community = subgraph.number_of_edges()
    num_nodes_within_community = subgraph.number_of_nodes()
    return num_edges_within_community / (num_nodes_within_community * (num_nodes_within_community - 1) / 2)

for idx, community_nodes in communities.items():
    dens = density(G, community_nodes)
    print(f"Community {idx} - Density:", dens)

# Centrality Calculation (Average Degree Centrality)
def average_degree_centrality(graph, community):
    degree_centralities = nx.degree_centrality(graph)
    return sum(degree_centralities[node] for node in community) / len(community)

for idx, community_nodes in communities.items():
    avg_degree_centrality = average_degree_centrality(G, community_nodes)
    print(f"Community {idx} - Average Degree Centrality:", avg_degree_centrality)
