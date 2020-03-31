from abc import ABC, abstractmethod
import numpy as np
import statistics as stats
import pandas as pd
from copy import deepcopy

from SumEMFields import EMFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from ParticleBunchClass import ParticleBunch

class AbstractSimulationClass(ABC):
    """ This class will be the abstract class that will define 
    the required methods for any Simulation class.
    """
    def __init__(self, totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=1.0, largeTimestep=1e-3
    , smallTimestep=1e-8):
        self.totalEMField = totalEMField
        self.particleBunch = particleBunch
        self.duration = duration
        self.largeTimestep = largeTimestep
        self.smallTimestep = smallTimestep

    @abstractmethod
    def RunSimulation(self):
        """ This method will run the simulation. 
        The method will be different for the different type of simulation
        that is being run.
        """
    
    @abstractmethod
    def SaveSimulation(self, fileName:str):
        """ This method will save the simulation state.
        This will be different as different simulations will require
        different datasets to be saved.
        """
    


