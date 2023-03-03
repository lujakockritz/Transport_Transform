#%%
import sys
import os
import random
import pandas as pd
import networkx as nx
from scipy.stats import truncnorm

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
#from mesa.datacollection import DataCollector

#%%

# Add the parent directory to the system path
script_dir = os.path.dirname( __file__ )
processed_data_dir = os.path.join( script_dir, os.pardir, 'config' )
sys.path.append( processed_data_dir )

# Import the config module from the processed subfolder
import config

class UserAgent(Agent):
    def __init__(self, unique_id, model, group):
       super().__init__(unique_id, model)
       self.group = group 
       self.ice_attitude = self.truncated_normal(config.clusterData.loc['ICE',(self.group,'Mean')], config.clusterData.loc['ICE',(self.group,'SD')], 0, 10)         #TODO: check if bounds are correct
          
    def truncated_normal(self, mean, std, lower_bound, upper_bound):
        return truncnorm.rvs(
            (lower_bound - mean) / std, (upper_bound - mean) / std, loc=mean, scale=std
        )

    def step(self):
        print("Agent " + str(self.unique_id) + "  in group: " + self.group + " my ICE attitude: " + str(self.ice_attitude))


class TransportModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.prob_connect = config.str_experience
        self.schedule = RandomActivation(self)
        #self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)
        self.G = nx.Graph()
        self.G.add_nodes_from(range(0,self.num_agents))
        self.grid = NetworkGrid(self.G)
        self.create_agents()
        
    def create_agents(self):
        for i in range(self.num_agents):
            if i < self.num_agents * config.EL_share:
                group = "EL"

            elif i < self.num_agents * (config.EL_share + config.CP_share):
                group = "CP"

            else:
                group = "RT"

            agent = UserAgent(i, self, group)
            self.schedule.add(agent)
            #self.G.add_node(i)
            self.grid.place_agent(agent, i)

         # Create edges between agents
        for agent in self.schedule.agents:
            for other in self.schedule.agents:
                if agent != other:
                    if agent.group == other.group:
                        if random.random() < self.prob_connect:
                            self.G.add_edge(agent, other)            #TODO: add weight generation
                    else:
                        if random.random() < (self.prob_connect * 0.1):
                            self.G.add_edge(agent, other)
    
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


empty_model = TransportModel(10)
empty_model.step()



# %%
