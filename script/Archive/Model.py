# coding=System
from TransportAgent import *
from UserAgent import *
from config import *

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import pandas as pd
import random
import networkx as nx


class TransportTransformModel(Model):

    """


    :version:
    :author:
    """

    """ ATTRIBUTES

   

  agents  (private)

   

  environment  (private)

   

  transportation  (private)

   

  network_properties  (private)

   

  users  (private)

   

  road  (private)

   

  bike_path  (private)

   

  rails  (private)

   

  car_sharing_infra  (private)

  """

    def __init__(self):
        """


        @return  :
        @author
        """

        """
    call truncNormDistribute to initialize attitudes

    self.attitude.ICE == truncNormDistribute
    """

    def create_network(self, N):
        """


        @param  N : 
        @return  :
        @author
        """
        import mesa
        from mesa import Model, Agent
        from mesa.space import ContinuousSpace

        class NetworkModel(Model):
            def __init__(self, N, width, height):
                self.num_agents = N
                self.grid = ContinuousSpace(width, height, True)
                self.agents = [Agent(i, self) for i in range(self.num_agents)]

            def step(self):
                for a in self.agents:
                    a.step()
                self.connect_agents_by_distance()

            def connect_agents_by_distance(self):
                for a in self.agents:
                    for b in self.agents:
                        if a != b:
                            (x1, y1) = a.position
                            (x2, y2) = b.position
                            dist = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
                            if dist <= 10:
                                a.connect(b)

    def invest(self):
        """


        @return  :
        @author
        """
        pass

    def step(self):
        """


        @return  :
        @author
        """
        # Advance Step Counter
        self.currentStep += 1
