# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:03:01 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/ESWEEK21/Grappolo_Shuffle/')

import itertools
import math
import networkx as nx
import sys


#1 for #edge density, 0 for column density, 2 for #edge density naive
score_choice = 0      

def nodes_connected(u, v):
    return u in G.neighbors(v)

def score_edge_density_naive(l):
    score = 0
    total = 0
    for i,j in itertools.combinations(l, 2):
        total += 1
        
        if nodes_connected(i, j):
            score += 1        

    return score / total

def score_edge_density(l):
    num = 0
    deg = 0

    for i,j in itertools.combinations(l, 2):
        if nodes_connected(i, j):
            num += 1
            
    for i in l: 
        deg += G.degree(i)
        
    dnum = deg - num  

    return num / dnum

def score_column_density(l):
    nnz = 0
    cols = set()
    
    for i,j in itertools.permutations(l, 2):
        if nodes_connected(i, j):
            nnz += 1
            cols.add(j)
    
    return nnz / len(cols)


#filename = sys.argv[1]

filename = 'facebook_combined_modified.txt_Grappolo.edges' #_Degree_density.txt'

#filename = 'road-usroads.txt_Grappolo.edges'

#filename = 'Sample.txt'

#filename = 'Sample.txt_Edge_density.txt'

G = nx.read_edgelist(filename, nodetype = int)

num_blocks = math.ceil(G.number_of_nodes() / 64) #vertice / #threads per block

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

#with open('EdgeDensity.txt', 'w') as file:
#     file.write(json.dumps(scores))

reorder = []

for rank in scores.keys():
    start = rank * math.ceil(G.number_of_nodes() / num_blocks)
    end = start + math.ceil(G.number_of_nodes() / num_blocks) 
    
    for i in range(start,end ):
        if (i < len(offset)):
            reorder.append(offset[i])
            
            
mapping = {}

for vertex in range(len(offset)):
    mapping[reorder[vertex]] = vertex
    
G = nx.relabel_nodes(G, mapping)

if (score_choice == 1):
    nx.write_edgelist(G, filename + '_Edge_density.txt', data = False)
else:
    nx.write_edgelist(G, filename + '_Column_density.txt', data = False)

    
#filename = 'facebook_combined_modified.txt_Grappolo.edges_Degree_density.txt'
#
#G = nx.read_edgelist(filename, nodetype = int)    
    
start = 0
count = 1

step = math.ceil(G.number_of_nodes() / 8)

weights = []

while (count <= num_blocks):
    
    weight = []
    if (count < num_blocks):
        
        mc1 = 0
        mc2 = 0
        mc3 = 0
        mc4 = 0
        mc5 = 0
        mc6 = 0
        mc7 = 0
        mc8 = 0
        start = (count - 1) * math.ceil(G.number_of_nodes() / num_blocks)
        end = start + (math.ceil(G.number_of_nodes() / num_blocks)) 
        
        for node in offset[start:end]:
            for neighbor in G.neighbors(node):
                if (neighbor < start or neighbor > end):
                    if (neighbor <= step):
                        mc1 += 1
                    if (neighbor > step & neighbor <= 2 * step):
                        mc2 += 1
                    if (neighbor > 2 * step & neighbor <= 3 * step):
                        mc3 += 1
                    if (neighbor > 3 * step & neighbor <= 4 * step):
                        mc4 += 1
                    if (neighbor > 4 * step & neighbor <= 5 * step):
                        mc5 += 1
                    if (neighbor > 5 * step & neighbor <= 6 * step):
                        mc6 += 1
                    if (neighbor > 6 * step & neighbor <= 7 * step):
                        mc7 += 1
                    if (neighbor > 7 * step):
                        mc8 += 1
                        
        total = mc1 + mc2 + mc3 + mc4 + mc5 + mc6 + mc7 + mc8 + 1         
        
        weight.append(mc1 / total)
        weight.append(mc2 / total)
        weight.append(mc3 / total)
        weight.append(mc4 / total)
        weight.append(mc5 / total)
        weight.append(mc6 / total)
        weight.append(mc7 / total)
        weight.append(mc8 / total)
                    
        count += 1
        
        
    else:
        
        mc1 = 0
        mc2 = 0
        mc3 = 0
        mc4 = 0
        mc5 = 0
        mc6 = 0
        mc7 = 0
        mc8 = 0
        start = (num_blocks - 1) * math.ceil(G.number_of_nodes() / num_blocks)
        end = G.number_of_nodes()
        
        for node in offset[start:end]:
            for neighbor in G.neighbors(node):
                if (neighbor < start or neighbor > end):
                    if (neighbor <= step):
                        mc1 += 1
                    if (neighbor > step & neighbor <= 2 * step):
                        mc2 += 1
                    if (neighbor > 2 * step & neighbor <= 3 * step):
                        mc3 += 1
                    if (neighbor > 3 * step & neighbor <= 4 * step):
                        mc4 += 1
                    if (neighbor > 4 * step & neighbor <= 5 * step):
                        mc5 += 1
                    if (neighbor > 5 * step & neighbor <= 6 * step):
                        mc6 += 1
                    if (neighbor > 6 * step & neighbor <= 7 * step):
                        mc7 += 1
                    if (neighbor > 7 * step):
                        mc8 += 1
                    
        total = mc1 + mc2 + mc3 + mc4 + mc5 + mc6 + mc7 + mc8 + 1
                    
        weight.append(mc1 / total)
        weight.append(mc2 / total)
        weight.append(mc3 / total)
        weight.append(mc4 / total)
        weight.append(mc5 / total)
        weight.append(mc6 / total)
        weight.append(mc7 / total)
        weight.append(mc8 / total)
                  
       
        count += 1
        
#        print(total)
        
    weights.append(weight)
            
            
import csv     

with open("weightsgrappoloShuffleColNormalizedAccurate.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(weights) 
            
            
            
            
            
            
            
            
            