import networkx as nx
import numpy as np
import heapq as hq

def road_capacity(graph,highway_types = {'living_street': 0, 'unclassified':0 ,'residential' : 1 ,'tertiary':1, 'secondary': 2 ,'primary': 2,'road':1, 'motorway': 4,'service':0,'trunk':2,'motorway_link': 4,'trunk_link':4,'primary_link':2, 'secondary_link':2,'tertiary_link':1, 'motorway_junction':2,'virtual':0}): 
# Initialiser la capacité des rues dans le réseau
    
    for edge in graph.edges:
        info = graph.get_edge_data(edge[0],edge[1],edge[2])
        distance = info['length'] 
        road_type = info['highway'] # Type de rue
        num_of_lanes = info.get('lanes') # Nombre de voies
        capacity = 0
        if num_of_lanes != None:
            capacity = int(max(num_of_lanes))*distance//4 # Modélisation avec citadines (longeur moyenne = 4)
        else:
            if isinstance(road_type,list):
                road_type = road_type[0]
            capacity = highway_types[road_type]*distance//4
        nx.set_edge_attributes(graph,{edge: {'capacity': capacity}})

def BPR_Link_performance(t,f,c):
#   Fonction de coût (ou performance)
    return t*(1+0.15*(f/c)**4)

def road_cost(g,road,car_speed = 120):
#   Fonction qui met à jour le coût en temps d'une arête
    highwayMaxspeed = {'living_street':0 , 'unclassified': 0,'residential' : 20 ,'tertiary':30, 'secondary': 50,'primary': 50,'road':30, 'motorway': 100,'service':np.inf,'trunk':80,'motorway_link': 90,'trunk_link':70,'primary_link':40, 'secondary_link':40,'tertiary_link':20, 'motorway_junction':80,'virtual': 0}
    
    info = g.get_edge_data(road[0],road[1],road[2])
    length = info.get('length')
    maxspeed = info.get('maxspeed')
    road_type = info['highway']
    if isinstance(road_type,list):
        road_type = road_type[0]
    if info['capacity'] == 0 or info['flow'] == 0: # Si la rue est remplie (ajouter une condition sur le flot?)
        return np.inf
    if isinstance(maxspeed,list):
        speed = float(max(maxspeed))
    elif isinstance(maxspeed,(str,int,float)):
        speed = min(car_speed,float(maxspeed))
    else:
        speed = min((car_speed,highwayMaxspeed[road_type]))
    try:
        travel_time = length/(speed/3.6) #Calcul du temps d'un trajet simple en s
    except ZeroDivisionError:
        return np.inf # Modélisation: on ignore les rues non classfiées
    f = info['flow']
    c = info['capacity']
    return BPR_Link_performance(travel_time,f,c) # Fonction de coût qui dépend du flot circulant

def cost_to_graph(g,speed=120): # Initialisation de coût
    for edge in g.edges:
        nx.set_edge_attributes(g,{edge: {'cost': road_cost(g,edge,speed)}})

def path_cost(g,path): # Calcul du temps de trajet total
    sum = 0
    for road in path:
        cost = g.get_edge_data(road[0],road[1],road[2])['cost']
        if cost == np.inf:
            return np.inf
        else:
            sum += cost
    return sum
    
def graph_levels(g,source): # Distance minimale à la source
    return nx.shortest_paths.single_source_shortest_path_length(g,source)
    
def nodes_per_levels(max_level,levels): # Ajout d'une "grille" de niveau pour faciliter le balayage des nœuds
    nodes_in_levels = dict((k,[]) for k in range(max_level+1))
    for node in levels:
        nodes_in_levels[levels[node]].append(node)
    return nodes_in_levels
    
def incoming_all(g): # liste des arêtes entrantes pour chaque nœud
    def incoming(g,node):
        L = []
        for x in g.predecessors(node):
            keys = g.get_edge_data(x,node).keys()
            for key in keys:
                L.append((x,node,key))
        return L
    incoming_edges = dict((node,incoming(g,node)) for node in g.nodes)
    return incoming_edges

def exiting_all(g): # Liste des arêtes sortantes pour chaque nœuds
    def exiting(g,node):
        L = []
        for x in g.successors(node):
            keys = g.get_edge_data(node,x).keys()
            for key in keys:
                L.append((node,x,key))
        return L
    exiting_edges = dict((node,exiting(g,node)) for node in g.nodes)
    return exiting_edges
