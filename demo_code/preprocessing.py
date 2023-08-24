import networkx as nx
from networkx.readwrite import json_graph
import csv
import json
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='Pull in file names for graph')
parser.add_argument('--links', '-l', nargs=1, help='file name for list of links in "source target" format')
parser.add_argument('--nodes', '-n', nargs=1, help='file name for list of nodes in "id label" format')
parser.add_argument('--output', '-o', nargs=1, help='file name for the output file to store the processed graph')
parser.add_argument("--low", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Keep the low centrality edges")
parser.add_argument("--remove_nodes", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Calculate centrality for nodes instead of edges")


def is_all_same(dict):
    result = True
    last_item = None
    for k, v in dict.items():
        if last_item is None:
            last_item = v
        else:
            if v == last_item:
                result = False
                break
    return result


# Will take in a file name and return an array of dictionaries. The keys
# of the dictionaries will be defined by the headers of the file.
def load_dsv(file_name, dl=' ', no_same=False):
    results = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=dl)
        line_count = 0
        headers = []
        for row in csv_reader:
            if line_count == 0:
                print('Column names are {}'.format(", ".join(row)))
                headers = row
            else:
                row_dict = {}
                for i in range(len(headers)):
                    row_dict[headers[i]] = row[i]
                if (no_same):
                    # Check to make sure all the entries do not equal each other
                    if (is_all_same(row_dict)):
                        results.append(row_dict)
                else:
                    results.append(row_dict)
            line_count += 1
        print('Processed {} lines.'.format(line_count-1))
    return results


# Traverse through the graph nodes and remove any nodes that do not have any`
# connecting edges, in or out.
def remove_orphaned_nodes(G):
    count = 0
    node_keys = list(G.nodes().keys())
    for node_key in node_keys:
        # Since this is a dictionary, we shouldn't have problems with removing
        # nodes, hopefully.
        if G.degree(node_key) == 0:
            count += 1
            G.remove_node(node_key)
    if (count != 0):
        print('Remove {} nodes'.format(count))


# Given a graph and a dictionary of edge keys and centrality scores, remove all
# but len(nodes) edges with the highest centrality scores. If keep_low equals
# to true, it only keeps the lowest centrality scores.
def remove_edge_lowest_centrality(G, edges, keep_low):
    # Turn dictionary into list of tuples
    edges_tl = [(edge_key, score) for edge_key, score in edges.items()]

    # Sort in increasing order if we are keeping the high or decreasing if we
    # are keeping the low.
    if (keep_low):
        edges_tl.sort(key=lambda x: x[1], reverse=True)
    else:
        edges_tl.sort(key=lambda x: x[1])

    # Keep len(edges) - (len(nodes))
    edges_tl = edges_tl[:len(edges_tl)-len(G.nodes)]

    # Go through list and remove edges from graph
    for edge_key, _ in edges_tl:
        G.remove_edge(edge_key[0], edge_key[1])

    print('Removed {} edges'.format(len(edges_tl)))


# Given a graph and a dictionary of node keys and centrality scores, remove all
# but k nodes with the highest centrality scores. If keep_low equals to true, it
# only keeps the lowest centrality scores.
def remove_node_lowest_centrality(G, nodes, keep_low, k):
    # Turn dictionary into list of tuples
    nodes_tl = [(node_key, score) for node_key, score in nodes.items()]

    # Sort in increasing order if we are keeping the high or decreasing if we
    # are keeping the low.
    if (keep_low):
        nodes_tl.sort(key=lambda x: x[1], reverse=True)
    else:
        nodes_tl.sort(key=lambda x: x[1])

    # Go through list and remove nodes from graph
    for node_key, _ in nodes_tl:
        if G.has_node(node_key):
            G.remove_node(node_key)
            remove_orphaned_nodes(G)
        if G.number_of_nodes() <= k:
            break

    print('Removed {} nodes'.format(len(nodes_tl)))


def main():
    args = parser.parse_args()

    print('Loading data')
    links = load_dsv(args.links[0], no_same=True)
    nodes = load_dsv(args.nodes[0])

    print('Creating the graph')
    node_data = [(item['node'], {"label": item['label']}) for item in nodes]
    link_data = [(item['source'], item['target']) for item in links]
    graph = nx.DiGraph()
    graph.add_edges_from(link_data)
    graph.add_nodes_from(node_data)
    print('Nodes: {}'.format(graph.number_of_nodes()))
    print('Edges: {}'.format(graph.number_of_edges()))

    with open('email-Eu-core.json', 'w') as json_file:
        json.dump(json_graph.node_link_data(graph), json_file)

    if (args.remove_nodes):
        print('Calculate centrality of the nodes')
        node_centrality = nx.betweenness_centrality(graph)

        print('Remove all but 100 nodes.')
        remove_node_lowest_centrality(graph, node_centrality, args.low, 100)
    else:
        print('Calculate centrality of the edges')
        edge_centrality = nx.edge_betweenness_centrality(graph)

        print('Remove all but len(nodes) edges with the highest centrality scores.')
        remove_edge_lowest_centrality(graph, edge_centrality, args.low)

        print('Remove nodes that do not have edges')
        remove_orphaned_nodes(graph)

    print('Write results to a file')
    print('Nodes: {}'.format(graph.number_of_nodes()))
    print('Edges: {}'.format(graph.number_of_edges()))
    with open(args.output[0], 'w') as json_file:
        json.dump(json_graph.node_link_data(graph), json_file)

    return

if __name__ == '__main__':
    main()