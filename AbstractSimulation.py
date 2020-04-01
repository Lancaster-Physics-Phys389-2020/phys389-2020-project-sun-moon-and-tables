from abc import ABC, abstractmethod
import numpy as np
import statistics as stats
import pandas as pd
from copy import deepcopy

from SumEMFields import EMFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from ParticleBunchClass import ParticleBunch

class AbstractSimulationClass(ABC):
    """ Abstract base class for building a simulation or set of simulations
        
        Class Attributes:
            totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                fields that interact in the simulation.
            particleBunch (object: ParticleBunch): The bunch of particles that are moved
                throughout the simulation
            duration (float): Duration of each simulation
            largeTimeStep (float): The timestep that is used when on average, the bunch is
                outside of the accelerating electric field
            smallTimeStep (float): The shorter timestep that is used when on average, the
                bunch is inside of the accelerating electric field.

    """
    def __init__(self, totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=1.0, largeTimestep=1e-3
    , smallTimestep=1e-8):
        """ Constructor for any simulation child class.

            Args:
                totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                    fields that interact in the simulation.
                particleBunch (object: ParticleBunch): The bunch of particles that are moved
                    throughout the simulation
                duration (float): Duration of each simulation
                largeTimeStep (float): The timestep that is used when on average, the bunch is
                    outside of the accelerating electric field
                smallTimeStep (float): The shorter timestep that is used when on average, the
                    bunch is inside of the accelerating electric field.
        """
        self.totalEMField = totalEMField
        self.particleBunch = particleBunch
        self.duration = duration
        self.largeTimestep = largeTimestep
        self.smallTimestep = smallTimestep

    @abstractmethod
    def RunSimulation(self):
        """ Abstract method for running the simulation or set of simulations.
                Method is abstract as different simulations require very different
                steps.  
        """
    
    @abstractmethod
    def SaveSimulation(self, fileName:str):
        """ Abstract method for saving data from the simulation or set of simulations.
                Method is abtract since different simulations generate results in 
                different formats.
        """
    


