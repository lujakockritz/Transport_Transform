# coding=System
from TransportAgent import *
from config import *

from mesa import Agent
import scipy.stats as stats


class UserAgent(Agent):

    """


    :version:
    :author:
    """

    """ ATTRIBUTES

   

  bike_owner  (private)

   

  car_owner  (private)

   

  main_mode  (private)

   

  group  (private)

   

  GF_attitude  (private)

   

  ICE_attitude  (private)

   

  PT_attitude  (private)

   

  CF_attitude  (private)

  """

    def __init__(self, agent_number, group):
        """


        @return  :
        @author
        """

        self.agent_number = agent_number
        pass

    def choose_mode(self):
        """


        @return  :
        @author
        """
        pass

    def check_crowding(self):
        """


        @return UserAgent :
        @author
        """
        pass

    def socialize(self):
        """


        @return UserAgent :
        @author
        """
        pass

    def truncNormDistribute(self, minVal, maxVal, mu, sigma):
        dist = stats.truncnorm((minVal - mu) / sigma,
                               (maxVal - mu) / sigma, loc=mu, scale=sigma)

    def step(self):
        """
        choose mode
        see experience (state & crowding)
        socialize every X time steps
        update attitude (experience, social influence,)
        """
