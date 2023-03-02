#%%
import random
import pandas as pd
import networkx as nx
from scipy.stats import truncnorm

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
#from mesa.datacollection import DataCollector

#import networkx as nx

#Parameters
prob = 0.5
num_agents = 10

#Group data
el_prop = 0.195              #TODO: add this to a config section
cp_prop = 0.659
rt_prop = 0.146
"Read in data on attitudes per cluster from Wolf et al. (2019)"
clusterData = pd.read_csv("../data/processed/Cluster_data.CSV", delimiter=';', index_col = [0], header=[0,1])


class UserAgent(Agent):
    def __init__(self, unique_id, model, group):
       super().__init__(unique_id, model)
       self.group = group 
       self.ice_attitude = self.truncated_normal(clusterData.loc['ICE',(self.group,'Mean')], clusterData.loc['ICE',(self.group,'SD')], 0, 10)         #TODO: check if bounds are correct
          
    def truncated_normal(self, mean, std, lower_bound, upper_bound):
        return truncnorm.rvs(
            (lower_bound - mean) / std, (upper_bound - mean) / std, loc=mean, scale=std
        )

    def step(self):
        print("Agent " + str(self.unique_id) + "  in group: " + self.group + " my ICE attitude: " + str(self.ice_attitude))


class TransportModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        #self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)
        self.grid = NetworkGrid(self.G)
        self.create_agents()
        
    def create_agents(self):
        for i in range(self.num_agents):
            if i < self.num_agents * el_prop:
                group = "EL"

            elif i < self.num_agents * (el_prop + cp_prop):
                group = "CP"

            else:
                group = "RT"

            agent = UserAgent(i, self, group)
            self.schedule.add(agent)
            self.grid.place_agent(agent)

         # Create edges between agents
        for agent in self.schedule.agents:
            for other in self.schedule.agents:
                if agent != other:
                    if agent.group == other.group:
                        if random.random() < prob:
                            self.grid.add_edge(agent, other)            #TODO: add weight generation
                    else:
                        if random.random() < prob * 0.1:
                            self.grid.add_edge(agent, other)
    
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


empty_model = TransportModel(num_agents)
empty_model.step()



# %%
