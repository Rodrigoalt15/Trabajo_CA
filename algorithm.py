import networkx as nx
import osmnx as ox
import pandas as pd  

class algorithm:
    def __init__(self, place):
        self.graph = ox.graph_from_place(place, network_type='drive')
        self.graph_edit=nx.DiGraph(self.graph)
        self.nodes, self.edges = ox.graph_to_gdfs(self.graph)
        self.path_layer_list = []

    def set_nearest_node(self, marker , x, y):
        marker.nearest_node = ox.distance.nearest_nodes(self.graph, x, y)
        print(marker.nearest_node)
        print(x)
        return marker.nearest_node

    def handle_change_location(self, marker1, marker2):
        shortest_path = nx.dijkstra_path(self.graph_edit, marker1, marker2, weight='length')  
        shortest_path_points = self.nodes.loc[shortest_path]
        return shortest_path_points

    def leer_archivo(self, path):
        path.to_csv('ruta.csv', index=False)
        df = pd.read_csv('ruta.csv')
        y = list(df["y"])
        x = list(df["x"])
        return y , x

    def eliminar_calle(self, nombre):
        self.edges = self.edges[self.edges['name']!= nombre]
        self.graph_edit=ox.graph_from_gdfs(self.nodes,self.edges)