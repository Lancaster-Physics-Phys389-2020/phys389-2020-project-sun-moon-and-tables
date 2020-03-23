import numpy as np
from AbstractExternalField import AbstractExternalFieldClass
import math

class ElectricExternalFieldClass(AbstractExternalFieldClass):
    """ This class will generate an external electric field that can vary
    sinosoidally with time, but each x,y and z currently have the same 
    function. Perhaps some way of changing that on the fly, giving frequency
    as a vector rather than as a float?
    """

    def __init__(self, electricFieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, name='Electric External Field'):
        super().__init__(fieldStrength=electricFieldStrength
        , angularFrequency=angularFrequency, name=name)
        self.fieldStrength = electricFieldStrength
        self.angularFrequency = angularFrequency
        self.name = name
        
    def __repr__(self):
        return 'Field Name: {0}, Angular Frequency: {1}, Electric Field Strength: {2}'.format(
        self.name, self.angularFrequency, self.fieldStrength)
    
    def generateField(self, timeElapsed):
        return super().generateField(timeElapsed)