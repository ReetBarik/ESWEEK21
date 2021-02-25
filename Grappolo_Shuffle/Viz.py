# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:48:16 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/ESWEEK21/Grappolo_Shuffle/')

import itertools
import math
import networkx as nx
import sys

import matplotlib.pyplot as plt
import numpy as np

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

offset = list(range(G.number_of_nodes()))

scores = []

start = 0
count = 1

while (count <= num_blocks):
    if (count < num_blocks):
        
        start = (count - 1) * math.ceil(G.number_of_nodes() / num_blocks)
        end = start + (math.ceil(G.number_of_nodes() / num_blocks)) 
        if (score_choice == 1):
            scores.append(score_edge_density(offset[start:end]))
        else:
            scores.append(score_column_density(offset[start:end]))
       
        count += 1
        
    else:
        
        start = (num_blocks - 1) * math.ceil(G.number_of_nodes() / num_blocks)
        end = G.number_of_nodes()
        if (score_choice == 1):
            scores.append(score_edge_density(offset[start:end]))
        else:
            scores.append(score_column_density(offset[start:end]))           
       
        count += 1




plt.hist(scores, density = False, bins = 10)  # density=False would make counts
plt.xlabel('Scores')
plt.ylabel('#Blocks')
plt.title("Facebook R:Grappolo S:Edge")
plt.ylim(0, 25)
plt.savefig('Facebook_Grappolo_1.png', dpi = 500)




























