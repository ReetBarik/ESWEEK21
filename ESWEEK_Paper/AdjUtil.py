# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:49:55 2021

@author: reetb
"""

import os
os.chdir('C:\\Users\\reetb\\Desktop\\ESWEEK_Paper')

import networkx as nx
from matplotlib import pyplot, patches
from scipy import io
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from networkx.utils import reverse_cuthill_mckee_ordering

def draw_adjacency_matrix(G, name, node_order=None, partitions=[], colors=[]):
    """
    - G is a netorkx graph
    - node_order (optional) is a list of nodes, where each node in G
          appears exactly once
    - partitions is a list of node lists, where each node in G appears
          in exactly one node list
    - colors is a list of strings indicating what color each
          partition should be
    If partitions is specified, the same number of colors needs to be
    specified.
    """
#    if (name == 1):
#        l = list(sorted(G.degree, key = lambda x: x[1], reverse = False))
#        deg = []
#        for i in l:
#            deg.append(i[0])
#        adjacency_matrix = nx.adjacency_matrix(G, nodelist=deg)
    if (name == 1):
        rcm = list(reverse_cuthill_mckee_ordering(G))
        adjacency_matrix = nx.adjacency_matrix(G, nodelist=rcm)
    else:
        adjacency_matrix = nx.adjacency_matrix(G, nodelist=node_order)
    adjacency_matrix = adjacency_matrix.todense()
    fig, ax = plt.subplots()

    # define the colors
    cmap = mpl.colors.ListedColormap(['w', 'k'])
    
    # create a normalize object the describes the limits of
    # each color
    bounds = [0., 0.5, 1.]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
    # plot it
    plt.xticks(np.arange(0, 28, 2))
    plt.yticks(np.arange(0, 28, 2))
    ax.imshow(adjacency_matrix, interpolation='none', cmap=cmap, norm=norm)
    fig.savefig(str(name) + '.png', dpi = 500)
    
            
            
filename = ['ToyEdgelist.txt', 'ToyEdgelist.txt', 'ToyEdgelist.txt_Grappolo.edges', 'ToyEdgelist.txt_Gorder.edges']            

for i in range(0,2):
    G = nx.read_edgelist(filename[i], nodetype = int)
    draw_adjacency_matrix(G, i)