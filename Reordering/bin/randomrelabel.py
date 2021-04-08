import networkx as nx
import sys
import random


filename = sys.argv[1]

G = nx.read_edgelist(filename, nodetype = int)

vertices = list(range(G.order()))

random.shuffle(vertices)

mapping = {}

for i in range(len(vertices)):
    mapping[i] = vertices[i]

G = nx.relabel_nodes(G, mapping)

G = nx.convert_node_labels_to_integers(G, first_label = 0)

nx.write_edgelist(G, filename, data = False)