#%%
import mesa
import pandas as pd
from scipy.stats import truncnorm


#Group data
el_prop = 0.195              #TODO: add this to a config section
cp_prop = 0.659
rt_prop = 0.146
"Read in data on attitudes per cluster from Wolf et al. (2019)"
clusterData = pd.read_csv("../data/processed/Cluster_data.CSV", delimiter=';', index_col = [0], header=[0,1])


class UserAgent(mesa.Agent):
    def __init__(self, unique_id, model, group):
       super().__init__(unique_id, model)
       self.group = group 

    def step(self):
        print("Hi, I am agent " + str(self.unique_id) + " and I am in group: " + self.group)

    #def truncated(self, mean, std, lower_bound, upper_bound):
    #    return truncnorm.rvs(
    #        (lower_bound - mean) / std, (upper_bound - mean) / std, loc=mean, scale=std
    #    )


class TransportModel(mesa.Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        #self.grid = mesa.grid.NetworkGrid({})
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
            #self.grid.add_node(agent)
    
    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

#%%
empty_model = TransportModel(10)
empty_model.step()
#%%