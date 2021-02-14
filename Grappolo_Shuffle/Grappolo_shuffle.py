# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:03:01 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/ArchitectureCollab/Grappolo_Shuffle/')

import itertools
import math
import networkx as nx
import sys


#1 for #edges, 0 for column density
score_choice = 1       

def nodes_connected(u, v):
    return u in G.neighbors(v)

def score_edge_density(l):
    score = 0
    total = 0
    for i,j in itertools.combinations(l, 2):
        total += 1
        
        if nodes_connected(i, j):
            score += 1        

    return score / total


def score_column_density(l):
    nnz = 0
    cols = set()
    
    for i,j in itertools.permutations(l, 2):
        if nodes_connected(i, j):
            nnz += 1
            cols.add(j)
    
    return nnz / len(cols)


#filename = sys.argv[1]

filename = 'facebook_combined_modified.txt_Grappolo.edges'
#filename = 'Sample.txt'
num_blocks = 56

G = nx.read_edgelist(filename, nodetype = int)

#A = nx.to_scipy_sparse_matrix(G, format = 'csr')

offset = list(range(G.number_of_nodes()))

scores = {}

start = 0
count = 1

while (count <= num_blocks):
    if (count < num_blocks):
        
        start = (count - 1) * math.ceil(G.number_of_nodes() / num_blocks)
        end = start + (math.ceil(G.number_of_nodes() / num_blocks)) 
        if (score_choice == 1):
            scores[count - 1] = score_edge_density(offset[start:end])
        else:
            scores[count - 1] = score_column_density(offset[start:end])
       
        count += 1
        
    else:
        
        start = (num_blocks - 1) * math.ceil(G.number_of_nodes() / num_blocks)
        end = G.number_of_nodes()
        if (score_choice == 1):
            scores[count - 1] = score_edge_density(offset[start:end])
        else:
            scores[count - 1] = score_column_density(offset[start:end])           
       
        count += 1
        
scores = dict(sorted(scores.items(), key=lambda item: item[1]))

reorder = []

for rank in scores.keys():
    start = rank * math.ceil(G.number_of_nodes() / num_blocks)
    end = start + math.ceil(G.number_of_nodes() / num_blocks) 
    
    for i in range(start,end ):
        if (i < len(offset)):
            reorder.append(offset[i])
            
            
mapping = {}

for vertex in range(len(offset)):
    mapping[vertex] = reorder[vertex]
    
G = nx.relabel_nodes(G, mapping)

if (score_choice == 1):
    nx.write_edgelist(G, filename + '_Edge_density.txt', data = False)
else:
    nx.write_edgelist(G, filename + '_Column_density.txt', data = False)

        
            
            
            
            
            
            
            
            
            
            
            
            