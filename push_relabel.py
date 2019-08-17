import networkx as nx
import random as rd
import numpy as np
import networkx.generators.random_graphs as randgen
import matplotlib.pyplot as plt
import queue
import osmnx as ox
import os
import sys
import requests
import json
os.chdir(r'C:\Users\Admin\Desktop\usb\Projects\TIPE')
from Vehicles import Car
import osmnx.save_load as sl


def init_preflot(g,s):
    e = dict((node,0) for node in g.nodes)
    h = e.copy()
    f = dict((edge,0) for edge in g.edges)
    f.update(dict((tuple(reversed(edge)),0) for edge in g.edges))
    h[s] = len(g.nodes)
    for node in g.successors(s):
        c = g.get_edge_data(s,node)['capacity']
        f[(s,node)] = c
        f[(node,s)] = -c
        e[node] = c
        e[s] -= c
    height_of_nodes = [[] for _ in range(len(g.nodes)+1)]
    higher_nodes = dict((node,list(g.nodes)) for node in g.nodes)
    return e,h,f,height_of_nodes,higher_nodes

def push(u,v):
    c = g.get_edge_data(u,v)['capacity']
    d = min(e[u],c-f[(u,v)])
    f[(u,v)] += d
    f[(v,u)] = -f[(u,v)]
    e[u] -= d
    e[v] += d

def relabel(residual,u):
    h[u] = 1 + min(h[v] for v in residual)
    
def init_overflow(g,e):
    overflow = set()
    for u in g.nodes:
        if e[u] > 0:
            overflow.add(u)
    return overflow

def push_relabel(g,s,t):
    e,h,f,height_of_nodes,higher_nodes = init_preflot(g,s)
    residual = g.copy()
    overflow = init_overflow(g,e)
    while True:
        pass