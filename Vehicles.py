import networkx as nx
import os
os.chdir(r'C:\Users\Admin\Desktop\usb\Projects\TIPE')
from flowMax import dijkstra_multi_path

""" Approche orienté-objet, pour traiter chaque véhicules comme un objet individuel.
    Plus Réaliste et plus intéressant comme étude qu'une simple analyse de donnée et une prévision statique.
    Donnée supplémentaires: type (pour les études futures)
                            vitesse max (pour simuler les conditions routières et les performances distintes)
                            priorité (ex: ambulance, voiture de police) ont une priorité plus élevée)
"""
class Car(object):

    def __init__(self,type,speed,source,target,g):
        self.type = type
        self.max_speed = speed
        self.source = source
        self.target = target
        self.position = source
        self.path = dijkstra_multi_path(g,source,target,weight='cost')
        self.time = 0
        self.cost = 0
        self.priority = 0
        self.checkpoint = self.path[0]
        self.way = [source]
    
    def get_position(self):
        return self.position
    
    def get_speed(self):
        return self.max_speed
    
    def get_destination(self):
        return self.target
    
    def get_path(self):
        return self.path
    
    def get_cost(self):
        return self.cost
    
    def get_priority(self):
        return self.priority
        
    def get_time(self):
        return self.time
    
    def get_checkpoint(self):
        return self.checkpoint
    
    def set_position(self,waypoint):
        self.position = waypoint
    
    def set_priority(self,priority):
        self.priority = priority
    
    def set_time(self,time):
        self.time = time
    
    def set_cost(self,cost):
        self.cost= cost
    
    def set_path(self,path):
        self.path = path
    
    def set_checkpoint(self,checkpoint):
        self.checkpoint = checkpoint
    
    def get_way(self):
        return self.way