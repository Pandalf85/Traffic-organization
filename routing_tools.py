import networkx as nx
import numpy as np
import heapq as hq
import heapq as hq
from itertools import count
import queue
from FibonacciHeap import FibonacciHeap

def flow_path_search(g,start,target): # Parcours en largeur en terme de flot (pour la mise à jour)
    if start == target:
        return []
    L = dict((x,True) for x in g.nodes)
    path = dict((x,[]) for x in g.nodes)
    path[start].append((start,0))
    q = queue.Queue()
    q.put(start)
    while not q.empty():
        u = q.get()
        
        for x in g.successors(u):
            d = g.get_edge_data(u,x)
            for key in d.keys():
                if L[x] and d[key]['flow'] > 0: # Condition: flot non nul (et pas capacité résiduelle)
                    L[x] = False
                    path[x] = path[u]+[(x,key)]
                    q.put(x)
                    break
            L[u] = False
    path = path[target]
    roadmap = []
    for k in range(len(path)-1):
        roadmap.append((path[k][0],path[k+1][0],path[k+1][1]))
    return roadmap


def adapted_dijkstra(g, start, weight = 'cost'):
#   Dijkstra adapté à la structure de MultiDiGraph et le critère de coût
    c = count() # Pour éviter de comparer le même nœud
    L = dict((x,True) for x in g.nodes)
    path = dict((x,[]) for x in g.nodes)
    path[start].append((start,0))
    q = FibonacciHeap() # Initialisation de tas de comparaison {Tas de Fibonacci)
    seen = dict((x,np.inf) for x in g.nodes)
    seen [start] = 0 # List d'antécédents
    q.insert((0,next(c),start,0)) 
    while True:
        try:
            dist,_,u,_ = q.extract_min()
        except TypeError:
            break
        for v in g._succ[u]: # particularité du graphe orienté (successeurs)
            key = 0
            d = g._succ[u][v]
            estimated_cost = np.inf # ! MultiDiGraph, il faut vérifier toutes les clés
            for k in d.keys():
                cost = d[k][weight]
                if cost < estimated_cost:
                    estimated_cost = cost
                    key = k
            final_cost = dist + estimated_cost
            if final_cost < seen[v]:
                if L[v]:
                    L[v] = False
                seen[v] = final_cost
                q.insert((final_cost,next(c),v,k)) # Algorithme de dijsktra classique
                path[v] = path[u] + [(v,k)] # La list garde à la fois le nœud et la clé de l'arête parcourue
        L[u] = False
    return path


def dijkstra_multi_path(g,start,target,weight = 'cost'):
# Fonction qui met le chemin sous forme de liste d'arêtes à parcourir (au lieu de nœuds)
    p = adapted_dijkstra(g,start,weight)[target]
    L = []
    for k in range(len(p)-1):
        L.append((p[k][0],p[k+1][0],p[k+1][1]))
    return L