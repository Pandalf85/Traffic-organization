import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import queue
import osmnx as ox
import os
import folium
os.chdir(r'C:\Users\Admin\Desktop\usb\Projects\TIPE')
import osmnx.save_load as sl
import timeit
from graph_management import *
from routing_tools import *

class Path_NotFound(Exception):
#   Signaler l'absence de chemin
    pass

class Saturated_Road(Exception):
#   Signaler l'apparition d'une saturation (blocage par le feu de trafic)
    pass


def bfs(g,start):
#   Recherche en largeur\Breadth first search
    L = dict((x,True) for x in g.nodes)
    path = dict((x,[]) for x in g.nodes)
    path[start].append((start,0))
    q = queue.Queue()
    q.put(start)  # File pour enregistré les sommets dans l'étape actuelle du parcours
    while not q.empty():
        u = q.get()
      
        for x in g.successors(u): # particularité du graphe orienté
            d = g.get_edge_data(u,x)
            for key in d.keys():
                if L[x] and d[key]['capacity'] - d[key]['flow'] > 0:
                    L[x] = False # i.e Le parcours a déjà passé par le sommet x
                    path[x] = path[u]+[(x,key)]
                    q.put(x)
                    break
        L[u] = False
    return path
    
def path_finding(g,start,target):
    path = bfs(g,start)
    
    if path[target] == []:
      raise Path_NotFound # Si la desination n'est pas relié au point de départ,il n'y a pas de chemin améliorant
    
    else:
      return path[target] # Le plus court chemin améliorant entre le point de départ et la destination
      
def edges_of_path(g,start,target):
    p = path_finding(g,start,target)
    L = []
    for k in range(len(p)-1):
        L.append((p[k][0],p[k+1][0],p[k+1][1]))
    return L # Donner le chemin sous forme de liste d'arêtes

def EDK(g,source,target,flow = 'flow'): # Algorithme d'Edmonds-Karp
    nx.set_edge_attributes(g,0,'flow')
    while True:
        try:
            path = edges_of_path(g,source,target)
            # Recherche de chemin améliorant via BFS
            cf = []
            for edge in path:
                d = g.get_edge_data(edge[0],edge[1],edge[2])
                cf.append(d['capacity']-d[flow])
            cfp = min(cf) # Calcul de capacité résiduelle du chemin
            for edge in path:
                f = cfp + g.get_edge_data(edge[0],edge[1],edge[2])[flow]
                nx.set_edge_attributes(g,{edge:{flow: f}}) # modification de flow
        except Path_NotFound: # Il n'y a plus de chemin améliorant, flot max atteint
            break


def flowUpdatePlus(g,source,target,edge):
    cap = g.get_edge_data(edge[0],edge[1],edge[2])['capacity']
    nx.set_edge_attributes(g,{(edge[0],edge[1],edge[2]): {'capacity':cap + 1}}) # Augmentation de capacité
    # En réalité, une seule boucle suffit
    try:
        path = edges_of_path(g,source,target)
        cf = []
        for edge in path:
            d = g.get_edge_data(edge[0],edge[1],edge[2])
            cf.append(d['capacity']-d['flow'])
        cfp = min(cf) # En réalité, la capacité résiduelle ne peut dépasser 1
        for edge in path:
            f = cfp + g.get_edge_data(edge[0],edge[1],edge[2])['flow']
            nx.set_edge_attributes(g,{edge:{'flow': f }})
            nx.set_edge_attributes(g,{edge:{'cost': road_cost (g,edge)}})  # Maintien du flot max
    except Path_NotFound:
        pass

def flowUpdateMinus(g,source,target,edge):
    info = g.get_edge_data(edge[0],edge[1],edge[2])
    if info['capacity'] == 0 or info['flow'] == 0:
        raise Saturated_Road
    else:
        if info['capacity'] > info['flow']: # Si la capacité n'est pas limitante
            nx.set_edge_attributes(g,{edge:{'capacity': info['capacity']-1}})
            nx.set_edge_attributes(g,{edge:{'cost':road_cost(g,edge)}}) 
        else:  # Si la capacité est limitante, il faut réduire le flot
            nx.set_edge_attributes(g,{edge:{'flow':info['flow']-1,'capacity':info['capacity']-1}})
            nx.set_edge_attributes(g,{edge:{'cost':road_cost(g,edge)}})
            try: # Redirection de flot
                path = edges_of_path(g,edge[0],edge[1])
                for road in path:
                    f = 1 + g.get_edge_data(road[0],road[1],road[2])['flow']
                    nx.set_edge_attributes(g,{road:{'flow': f }})
                    nx.set_edge_attributes(g,{road:{'cost': road_cost (g,road)}})
            except Path_NotFound: # On ne peut pas rediriger le flot, il faut alors diminuer le flot total
                first_path = flow_path_search(g,source,edge[0])
                second_path = flow_path_search(g,edge[1],target)
                path = first_path + second_path
                for road in path: # Conservation du flot
                    d = g.get_edge_data(road[0],road[1],road[2])
                    nx.set_edge_attributes(g,{road:{'flow': d['flow']-1}})
                    nx.set_edge_attributes(g,{road:{'cost':road_cost(g,road)}})


gp = sl.load_graphml('Paris_no_res.json',r'C:\Users\Admin\Desktop\usb\Projects\TIPE')
sm = 1143095752
ce = 1757030783
# sm2 = 24984454


def timer():
    k = timeit.Timer('EDK(gp,1757030783,1143095752)','''from __main__ import EDK\nfrom __main__ import gp''')
    return k
# route_aller = nx.shortest_path(gp,ce,sm,'length')
# route_retour = nx.shortest_path(gp,sm,ce,'length')

# def flow_to_graph(graph,flow):
#     for edge in flow.keys():
#         nx.set_edge_attributes(graph,{(edge[0],edge[1],edge[2]): {'flow': flow[edge]}})

# gp = ox.graph_from_place('Saint-Maur-des-Fossés, Val-de-Marne, France',network_type = 'drive')
# 299573246,319094661
