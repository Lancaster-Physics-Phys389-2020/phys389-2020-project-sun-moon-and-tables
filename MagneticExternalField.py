import numpy as np
from AbstractExternalField import AbstractExternalFieldClass
import math

class MagneticExternalFieldClass(AbstractExternalFieldClass):
    """ This class will generate an external eagnetic field that can vary
    sinosoidally with time, but each x,y and z currently have the same 
    function. Perhaps some way of changing that on the fly, giving frequency
    as a vector rather than as a float?
    """

    def __init__(self, magneticFieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, name='Magnetic External Field'):
        super().__init__(fieldStrength=magneticFieldStrength
        , angularFrequency=angularFrequency, name=name)
        self.fieldStrength = magneticFieldStrength
        self.angularFrequency = angularFrequency
        self.name = name
        
    def __repr__(self):
        return 'Field Name: {0}, Angular Frequency: {1}, Magnetic Field Strength: {2}'.format(
        self.name, self.angularFrequency, self.fieldStrength)
    
    def generateField(self, timeElapsed):
        return super().generateField(timeElapsed)