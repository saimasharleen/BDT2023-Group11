import pandas as pd
import networkx as nx
from node2vec import Node2Vec

# Load the dataset (replace 'path_to_dataset' with the actual path)
data = pd.read_csv("/Users/saimasharleen/PycharmProjects/pythonProject1/facebook_combined.txt", sep=' ', header=None, names=['user1', 'user2'])

# Create an empty undirected graph
G = nx.Graph()

# Add edges from the dataset to the graph
for row in data.itertuples(index=False):
    G.add_edge(row.user1, row.user2)

# Create an instance of Node2Vec
node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=4)

# Perform the random walks and generate the embeddings
model = node2vec.fit(window=10, min_count=1)

# Define the link prediction task (example with node '279' as the source node)
source_node = 279
target_nodes = [280, 281, 282]  # Replace these with the nodes you want to predict links for

# Check if the source and target nodes exist in the model's vocabulary
missing_nodes = [node for node in [source_node] + target_nodes if str(node) not in model.wv.key_to_index]
if missing_nodes:
    raise ValueError(f"Nodes {missing_nodes} not found in the embedding model vocabulary.")

# Compute similarities between the source node and target nodes
similarities = {}
for target_node in target_nodes:
    similarity = model.wv.similarity(str(source_node), str(target_node))
    similarities[target_node] = similarity

# Sort the similarities in descending order to get the most similar nodes first
sorted_similarities = dict(sorted(similarities.items(), key=lambda item: item[1], reverse=True))

# Display the sorted similarities
print("Sorted similarities:")
for target_node, similarity in sorted_similarities.items():
    print(f"Node {source_node} and Node {target_node}: {similarity:.4f}")
