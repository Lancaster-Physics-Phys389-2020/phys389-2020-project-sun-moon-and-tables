import numpy as np
import math
import scipy
from GenericField import GenericFieldClass
from abc import ABC, abstractmethod

class AbstractExternalFieldClass(ABC, GenericFieldClass):
    """ This class will have the parameters and functions that all external, time
    varying fields will have. This will then allow a magnetic and electric field
    class to inherit from these, which will both be quite similar classes
    """

    def __init__(self, fieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0
    , listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Abstract External Field'):
        self.fieldStrength = fieldStrength
        self.angularFrequency = angularFrequency
        self.name = name
        self.listOfDimensions = listOfDimensions

    @abstractmethod 
    def __repr__(self):
        return 'Field: {0}, Angular Frequency: {1}, Field Strength: {2}\
            Dimensions of the Field: {3}'.format(self.name
            , self.angularFrequency, self.fieldStrength, self.listOfDimensions)
    # should this be an abstract method? The repr does need to be different for
    # the electric and magnetic fields.. but this is the standard structure I
    # want it to have.

    def IsParticleInField(self, affectedParticle):
        # so this checks if the affectedparticle by the field is within the field
        # and this also applies to electric and magnetic fields, which is neat.
        isInFieldArray = np.array([1.0, 1.0, 1.0])
        for i in range(3):
            if not (affectedParticle.position[i] > self.listOfDimensions[i][0]
            and affectedParticle.position[i] < self.listOfDimensions[i][1]):
                isInFieldArray[i] = 0.0
        return isInFieldArray
           
    def GenerateField(self, timeElapsed, affectedParticle):
        # calls isParticleInField to determine if the affected particle
        # is hit by the electric or magnetic field. multiplies the "truth array"
        # for the dimensions of the field by the time dependence for the field.
        return (math.cos(self.angularFrequency * timeElapsed) 
        * np.multiply(AbstractExternalFieldClass.IsParticleInField(self, affectedParticle)
        , self.fieldStrength))
