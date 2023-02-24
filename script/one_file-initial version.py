import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
from scipy.stats import truncnorm


class UserAgent(Agent):
    def __init__(self, unique_id, model, group, ice_mean, ice_std, pr_mean, pr_std):
        """
        Create a new user agent.

        Args:
            unique_id (int): Unique identifier for the agent.
            model (TransportTransform): The model that the agent belongs to.
            group (str): The group that the agent belongs to.
            ice_mean (float): Mean of the truncated normal distribution for ICE attitude.
            ice_std (float): Standard deviation of the truncated normal distribution for ICE attitude.
            pr_mean (float): Mean of the truncated normal distribution for PR attitude.
            pr_std (float): Standard deviation of the truncated normal distribution for PR attitude.
        """
        super().__init__(unique_id, model)
        self.group = group

        # Initialize attitudes for transportation modes
        self.ice_attitude = self.truncated_normal(ice_mean, ice_std, 0, 10)
        self.pr_attitude = self.truncated_normal(pr_mean, pr_std, 0, 10)

    def step(self):
        """
        Update the agent's state.
        """
        # Update code for each time step goes here
        pass

    def truncated_normal(self, mean, std, lower_bound, upper_bound):
        """
        Generate a truncated normal random variable.

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


class TransportTransform(Model):
    def __init__(
        self,
        num_agents,
        el_prop=0.195,
        cp_prop=0.659,
        rt_prop=0.146,
        prob_connect=0.5,
        el_ice_mean=4.56,
        el_ice_std=0.89,
        el_pr_mean=4.2,
        el_pr_std=1,
        cp_ice_mean=4.18,
        cp_ice_std=0.94,
        cp_pr_mean=3.45,
        cp_pr_std=0.98,
    ):
        """
        Create a new transport transformation model.

        Args:
            num_agents (int): Number of agents in the model.
            el_prop (float): Proportion of agents in the EL group.
            cp_prop (float): Proportion of agents in the CP group.
            rt_prop (float): Proportion of agents in the RT group.
            prob_connect (float): Probability of an edge between two agents being created.
            el_ice_mean (float): Mean of the truncated normal distribution for ICE attitude in EL group.
            el_ice_std (float): Standard deviation of the truncated normal distribution for ICE attitude in EL group.
            el_pr_mean (float): Mean of the truncated normal distribution for PR attitude in EL group.
            el_pr_std (float): Standard deviation of the truncated normal distribution for PR attitude in EL group.
            cp_ice_mean (float): Mean of the truncated normal distribution for ICE attitude in CP group.
            cp_ice_std (float): Standard deviation of the truncated normal distribution for ICE attitude in CP group.
            cp_pr_mean (float): Mean of the truncated normal distribution for PR attitude in CP group.
            cp_pr_std (float): Standard deviation of the truncated normal distribution for PR attitude in CP group.
        """

        self.num_agents = num_agents
        self.el_prop = el_prop
        self.cp_prop = cp_prop
        self.rt_prop = rt_prop
        self.prob_connect = prob_connect
        self.el_ice_mean = el_ice_mean
        self.el_ice_std = el_ice_std
        self.el_pr_mean = el_pr_mean
        self.el_pr_std = el_pr_std
        self.cp_ice_mean = cp_ice_mean
        self.cp_ice_std = cp_ice_std
        self.cp_pr_mean = cp_pr_mean
        self.cp_pr_std = cp_pr_std

        self.schedule = RandomActivation(self)
        self.grid = NetworkGrid({})
        self.create_agents()

        # Create network visualization
        self.network = NetworkModule(self.grid.G, width=500, height=500, library='d3')
        self.visualization = ModularServer(self, [self.network], "TransportTransform")

    def create_agents(self):
        """
        Create agents for the simulation.

        Assigns each agent to a group based on the proportions specified in the constructor.
        Generates ICE and PR attitudes for each agent from truncated normal distributions with
        means and standard deviations specific to their group. Creates edges between agents based
        on their group and the probability of connection specified in the constructor.
        """
        for i in range(self.num_agents):
            if i < self.num_agents * self.el_prop:
                group = "EL"
                ice_mean = self.el_ice_mean
                ice_std = self.el_ice_std
                pr_mean = self.el_pr_mean
                pr_std = self.el_pr_std
            elif i < self.num_agents * (self.el_prop + self.cp_prop):
                group = "CP"
                ice_mean = self.cp_ice_mean
                ice_std = self.cp_ice_std
                pr_mean = self.cp_pr_mean
                pr_std = self.cp_pr_std
            else:
                group = "RT"
                ice_mean = np.random.uniform(0, 10)
                ice_std = 1
                pr_mean = np.random.uniform(0, 10)
                pr_std = 1

            agent = UserAgent(i, self, group, ice_mean, ice_std, pr_mean, pr_std)
            self

            agent = UserAgent(i, self, group)
            self.schedule.add(agent)
            self.grid.add_node(agent)

        # Create edges between agents
        for agent in self.schedule.agents:
            for other in self.schedule.agents:
                if agent != other:
                    if agent.group == other.group:
                        if random.random() < self.prob_connect:
                            self.grid.add_edge(agent, other)
                    else:
                        if random.random() < self.prob_connect * 0.1:
                            self.grid.add_edge(agent, other)

    def step(self):
        self.schedule.step()


# Example usage:
model = TransportTransform(1000)
model.visualization.port = 8521  # Set the port for the web server
model.visualization.launch()  # Launch the web server
for i in range(10):
    model.step()