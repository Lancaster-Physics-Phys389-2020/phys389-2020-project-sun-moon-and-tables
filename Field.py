import numpy as np
import math
import copy
import scipy.constants
from abc import ABC, abstractmethod
from Particle import Particle

#note for modelling the dimensions that a field exists in:
#source 1: http://archive.petercollingridge.co.uk/book/export/html/460
#could do it with this.. just might need a lot of rectangles. 
#but then you could turn off sections of the magnetic field individually, to accelerate
#particles and then shoot them out.
#ask bertram.

class AbstractFieldClass(ABC):
    """Class to model any field. Might need a parent class to help define where it comes from, 
    and to properly simulate things, might need a way of implementing a way of limiting where the
    field can act. Some kind of parent class that provides dimensions?
    For now, this will be a class that will apply some of the implementations that the electric
    and magnetic field classes will need. An abstract method for their acceleration, which come
    from different sources. 
    """

    def __init__():
        
    @abstractmethod
    def GiveAcceleration(self, TheParticle):
        pass