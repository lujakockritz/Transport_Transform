#%%
import sys
import os
import random
#import pandas as pd
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

"""
This script creates an agent-based model where user agents have an attitude towards varios transportation modes. 
The attitudes are set based on mean and standard deviation calculated based on empirical data pblished in this study:
Wolf, I., & Schröder, T. (2019). Connotative meanings of sustainable mobility: A segmentation approach using cultural sentiments. Transportation Research Part A: Policy and Practice, 126, 259–280. https://doi.org/10.1016/J.TRA.2019.06.002 

The model is initialized as a network where connections between group memebers are more likely than across group members.
Weights between agents are set based on similarity in their attitude using Euclidian Distance.
"""

class UserAgent(Agent):
    def __init__(self, unique_id, model, group):
       """
        Create a new user agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (TransportTransform): The model that the agent belongs to.
            group (str): The group that the agent belongs to.

        """
       super().__init__(unique_id, model)
       self.group = group 
       self.ice_attitude = self.truncated_normal(config.clusterData.loc['ICE',(self.group,'Mean')], config.clusterData.loc['ICE',(self.group,'SD')], 0, 10)         #TODO: check if bounds are correct
          
    def truncated_normal(self, mean, std, lower_bound, upper_bound):
        """
        Generate a truncated normal random variable. Truncated normal distribution is chosen because #TODO add arguments 

        Args:
            mean (float): Mean of the truncated normal distribution.
            std (float): Standard deviation of the truncated normal distribution.
            lower_bound (float): Lower bound for the truncated normal distribution.
            upper_bound (float): Upper bound for the truncated normal distribution.

        Returns:
            float: A truncated normal random variable.
        """
        return truncnorm.rvs(
            (lower_bound - mean) / std, (upper_bound - mean) / std, loc=mean, scale=std
        )

    def step(self):
        """
        Update the agent's state.
        """
        print("Agent " + str(self.unique_id) + "  in group: " + self.group + " my ICE attitude: " + str(self.ice_attitude))


class TransportModel(Model):
    def __init__(self, N):
        """
        Create a new transport transformation model.

        Args:
            num_agents (int): Number of agents in the model.
            prob_connect (float): Probability of an edge between two agents being created.
        """
        self.num_agents = N
        self.prob_connect = config.str_experience
        self.schedule = RandomActivation(self)
        #self.G = nx.erdos_renyi_graph(n=self.num_agents, p=prob)
        self.G = nx.Graph()
        self.G.add_nodes_from(range(0,self.num_agents))
        self.grid = NetworkGrid(self.G)
        self.create_agents()
        self.calculate_weight()
        
    def create_agents(self):
        """
        Create agents for the simulation.

        Assigns each agent to a group based on the proportions specified in the constructor.
        Creates edges between agents based on their group and the probability of connection 
        specified in the constructor.
        """
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
    
    def calculate_weight(self, modes=["ICE"]):            #TODO: add this when the edges are created TODO: make this flexible for the number of modes
        """
        Calculates the weight of the connections between the agents based on the Euclidean distance
        between their attitudes towards the given transportation modes.

        Args:
        modes (list of str): The transportation modes to include in the calculation.

        Returns:
            float: The total weight of the connections between the agents.
        """
        #total_weight = 0
        for agent in self.schedule.agents:
            neighbors = []
            for neighbor in self.grid.get_neighbors(agent, include_center=False):
                #diffs = [abs(getattr(agent, mode) - getattr(neighbor, mode)) for mode in modes]
                #weight = np.sqrt(sum([diff ** 2 for diff in diffs]))
                #total_weight += weight
                neighbors.append(neighbor)
            print("I am node " + agent + " and my neighbors are " + neighbors)        
        #return total_weight
    
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()



empty_model = TransportModel(10)
empty_model.step()


# %%
