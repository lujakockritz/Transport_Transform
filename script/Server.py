#%%
import mesa
#import networkx as nx
#from mesa.visualization.modules import NetworkModule
#from mesa.visualization.ModularVisualization import ModularServer
#from mesa.visualization.UserParam import UserSettableParameter

# import the Base_Model class from the same folder
from Model import TransportModel

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
    #return {"nodes": node_dict, "edges": edge_list}

    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return {
            group.EL: '#FF0011',
            group.CP: '#FF0000',
            group.RT: '#008000'
        }.get(agent.group, '#808080')

    def edge_color(agent1, agent2):
        #if State.RESISTANT in (agent1.state, agent2.state):
        #    return '#000000'
        return '#e8e8e8'

    def edge_width(agent1, agent2):
        #if State.RESISTANT in (agent1.state, agent2.state):
        #    return 3
        return 2

    def get_agents(source, target):
        return G.node[source]['agent'][0], G.node[target]['agent'][0]

    portrayal = dict()
    portrayal['nodes'] = [{'size': 6,
                           'color': node_color(agents[0]),
                           'tooltip': "id: {}<br>state: {}".format(agents[0].unique_id, agents[0].state.name),
                           }
                          for (_, agents) in G.nodes]

    portrayal['edges'] = [{'source': source,
                           'target': target,
                           'color': edge_color(*get_agents(source, target)),
                           'width': edge_width(*get_agents(source, target)),
                           }
                          for (source, target) in G.edges]

    return portrayal

network = mesa.NetworkModule(network_portrayal, 500, 500)

# define the server
model_params = {
    'N': mesa.UserSettableParameter('slider', 'Number of agents', 10, 1, 100, 1),
}
server = mesa.ModularServer(TransportModel, [network], "Transport Model", model_params)

# launch the server
server.port = 8525 # choose any available port number
server.launch()
# %%
