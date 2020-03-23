import numpy as np
import math
from GenericField import GenericFieldClass
from abc import ABC, abstractmethod

class AbstractExternalFieldClass(ABC, GenericFieldClass):
    """ This class will have the parameters and functions that all external, time
    varying fields will have. This will then allow a magnetic and electric field
    class to inherit from these, which will both be quite similar classes
    """

    def __init__(self, fieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, name='Abstract External Field'):
        self.fieldStrength = fieldStrength
        self.angularFrequency = angularFrequency
        self.name = name

    @abstractmethod 
    def __repr__(self):
        return 'Field: {0}, Angular Frequency: {1}, Field Strength: {2}'.format(
            self.name, self.angularFrequency, self.fieldStrength)
    # should this be an abstract method? The repr does need to be different for
    # the electric and magnetic fields.. but this is the standard structure I
    # want it to have.

    def generateField(self, timeElapsed):
        return (math.cos(self.angularFrequency * timeElapsed) 
        * self.fieldStrength)
