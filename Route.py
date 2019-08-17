import os
import networkx as nx
import random as rd
import osmnx as ox
import osmnx.save_load as sl
import timeit
import heapq as hq
os.chdir(r'C:\Users\Admin\Desktop\usb\Projects\TIPE')
from flowMax import *
from FibonacciHeap import *
from Vehicles import *

number_of_jams = 0
saturation = 0

class JamOccurence(Exception):
#   Signaler l'apparition de congestion (i.e embouteillage total et non une simple saturation)
    pass

def cars_suite(number,type,speed,start,target,g):
#   Initialisation de trafic entrant
    L = []
    for _ in range(number):
        L.append(Car(type,speed,start,target,g))
    return L

def new_crossroads(g):
#   Initialisation des carrefours (nœuds)
    return dict((node,[]) for node in g.nodes)

def new_traffic(g):
#   Initialisation de l'état de trafic circulant (arêtes)
    return  dict((edge,[]) for edge in g.edges)


def charge_junction(g,junction,incoming_edges,traffic,crossroads,source,target):
#   Chargement des carrefours selon une stratégie prédéfinie
#   (Ici, les voitures qui ont une priorité plus élevée)
    if junction == source:
    # La source n'est pas chargée (Dans le cas d'un seul départ)
        pass
    else:
        entering_roads = incoming_edges[junction] # Toutes les arêtes entrantes du carrefour choisi
        q = crossroads[junction] # L'état de trafic du carrefour
        b = True 
        
        while b: # Condition: Il reste des voitures à distribuer
            
            b = False
            L = []
            
            for road in entering_roads:
            #   Choix d'ordre d'entrée pour les premières voitures devant le feu
                
                try:
                    car = traffic[road].pop(0)
                except IndexError:
                    continue # i.e Il n'y a plus de voitures dans cette rue
                
                print('%s went from %s to %s' % (car,str(car.position),str(junction)))
                # Impression du log pour suivre les évènements
                car.set_position(junction)
                # Transmission de l'information à l'objet 
                flowUpdatePlus(g,source,target,road)
                # La voiture part de sa rue précédente. Libération d'espace
                L.append(car)
                car.path.pop(0)
                car.way.append(road[1])
                # Suivi du chemin parcouru par la voiture
                b = True

            q += sorted(L,key = Car.get_cost) # Maintien de l'ordre de départ


def update_paths(g,crossroad,target):
    for car in crossroad:
        car.path = dijkstra_multi_path(g,car.position,target)


def departure_from_junction(g,junction,exiting_edges,traffic,crossroads,source,target,update):
#   Distribuer les voitures dans les arêtes sortantes selon l'ordre défini dans l'étape précédente
    global saturation
    if junction == target:
    # Le puits n'est pas sortant
        pass 
    else:
        exiting_roads = exiting_edges[junction]
        c = crossroads[junction]
        while 0 < len(c):
            car = c[0]
            road = car.get_path()[0]
            new_path = dijkstra_multi_path(g,junction,target)
            
            try:
                cost = g.get_edge_data(road[0],road[1],road[2])['cost']
                if cost == np.inf:
                    # S'il y a une saturation, l'itinéraire initial est bloqué.*
                    raise Saturated_Road
                if update[junction]:
                    cost *= 2
                flowUpdateMinus(g,source,target,road)
                car.set_cost(car.get_cost() + cost)
                print('%s traveled %f' % (car,cost)+'s')
                car.set_checkpoint(road)
                print('%s is currently rolling on %s' % (c[0],road))
                traffic[road].append(c[0])
                del c[0]
            
            except Saturated_Road:
                if new_path == []:
                    # Il y a un embouteillage lorsque pour la voiture sortante, il n'y a plus d'itinéraire disponible
                    print('Traffic jam at %s' % str(junction))
                    update[junction] = True
                    raise JamOccurence
                else:
                    saturation += 1
                    print('%s is saturated,updating paths...' % str(road))
                    update_paths(g,c,target)                    
        
    update[junction] = False        

def simulate(graph,number_of_cars,type,speed,source,target):
    global number_of_jams
    g = graph.copy()
    EDK(g,source,target)
    cost_to_graph(g)
    levels = graph_levels(g,source)
    max_level = max(levels.values())
    nodes_in_levels = nodes_per_levels(max_level,levels)
    incoming_edges = incoming_all(g)
    exiting_edges = exiting_all(g)
    traffic = new_traffic(g)
    crossroads = new_crossroads(g)
    crossroads[source] = cars_suite(number_of_cars,type,speed,source,target,g)
    compteur = 1
    k = 0
    update = dict((node,False) for node in g.nodes)
    while len(crossroads[target]) < number_of_cars:
        k = max_level
        while k >= 0:
            for junction in nodes_in_levels[k]:
                try:
                    departure_from_junction(g,junction,exiting_edges,traffic,crossroads,source,target,update)
                    charge_junction(g,junction,incoming_edges,traffic,crossroads,source,target)
                except JamOccurence:
                    number_of_jams += 1
            k -= 1
        print('Turn %d complete' % compteur)
        compteur += 1
        if compteur == 134:
            break
    return traffic,crossroads
s = 299573246
t = 319094661

def display_func(cars,func):
    L = []
    for car in cars:
        L.append(func(car))
    return L
# gs = sl.load_graphml('saintmaur',r'C:\Users\Admin\Desktop\usb\Projects\TIPE')
# road_capacity(gs)
# all = simulate(gs,5,'citadine',120,s,t)

# gp = ox.graph_from_place('Saint-Maur-des-Fossés, Val-de-Marne, France',network_type = 'drive')

# c = simulate(gp,1,'citadine',120,299573246,319094661)
# c = simulate(gp,1,'citadine',120,ce,sm)

sm = 1143095752
ce = 1757030783
sm2 = 24984454
