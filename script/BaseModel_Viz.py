#%%
#import mesa
import networkx as nx
from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

# import the Base_Model class from the same folder
from Base_Model import *

#%%
# define the visualization elements
def network_portrayal(G):
    # define how the network graph is drawn on the canvas
    # this function should return a dictionary with two keys:
    # "nodes": a dictionary mapping node IDs to their attributes
    # "edges": a list of dictionaries, each representing an edge and containing the keys "id1" and "id2"
    node_dict = {}
    for node in G.nodes:
        node_dict[node] = {"color": "red", "size": 5}
    edge_list = [{"id1": u, "id2": v} for u, v in G.edges]
    print({"nodes": node_dict, "edges": edge_list})
    return {"nodes": node_dict, "edges": edge_list}

network = NetworkModule(network_portrayal, 500, 500)

# define the server
model_params = {
    'N': UserSettableParameter('slider', 'Number of agents', 10, 1, 100, 1),
}
server = ModularServer(TransportModel, [network], "Transport Model", model_params)

# launch the server
server.port = 8522 # choose any available port number
server.launch()
# %%
