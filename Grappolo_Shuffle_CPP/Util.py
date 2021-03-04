# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 19:13:12 2021

@author: reetb
"""

import os
os.chdir('C:/Users/reetb/Desktop/NewDatasets/Output/Edgelists/Grappolo/')

import pandas as pd
import networkx as nx

df = pd.read_csv('twitter_combined.txt_Grappolo.edges', sep = ' ', header = None)

df.to_csv('twitter_combined.txt_Grappolo.edges', index=False)


#inputGraph = 'twitter_combined.txt_Grappolo.edges'
vertexList = 'TwitterReorder.txt'

def read_integers(filename):
    with open(filename) as f:
        return [int(x) for x in f]
    
    
vertices = read_integers(vertexList)

mapping = {}

for i in range(len(vertices)):
    mapping[vertices[i]] = i

df[0] = [mapping[i] for i in df[0]]
df[1] = [mapping[i] for i in df[1]]

df.to_csv('twitter_combined.txt_GrappoloShuffle.edges', index=False)
#
#for i in range(len(df)):
#    df[0][i] =  vertices[df[0][i]]
#    df[1][i] =  vertices[df[1][i]]

#G = nx.read_edgelist(inputGraph, nodetype = int)
#
mapping = {}

for i in range(len(vertices)):
    mapping[vertices[i]] = i
#    
#G = nx.relabel_nodes(G, mapping)
#
#nx.write_edgelist(G, inputGraph + 'Shuffle.edges', data = False)