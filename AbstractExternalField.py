import numpy as np
import math
import scipy
from GenericField import GenericFieldClass
from abc import ABC, abstractmethod

class AbstractExternalFieldClass(ABC, GenericFieldClass):
    """ Abstract base class for external electromagnetic fields that oscillate sinusoidally

    Class attributes:
            fieldStrength (ndarray): Amplitude of EM field in 3D space
            angularFrequency (float): Angular frequency of EM field 
            phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
            name (str): Name of EM field
            listOfDimensions (list): List of maximum and minimum dimensions
                of the field in 3D space
    """

    def __init__(self, fieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, phaseShift=0.0
    , listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Abstract External Field'):
        """ Constructor for any external EM field. Inherits the __init__ from GenericFieldClass
        
            Args:
                fieldStrength (ndarray): Amplitude of EM field in 3D space
                angularFrequency (float): Angular frequency of EM field 
                phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
                name (str): Name of EM field
                listOfDimensions (list): List of maximum and minimum dimensions
                    of the field in 3D space
        """
        super().__init__(name=name)
        self.fieldStrength = fieldStrength
        self.angularFrequency = angularFrequency
        self.phaseShift = phaseShift
        self.name = name
        self.listOfDimensions = listOfDimensions


    @abstractmethod 
    def __repr__(self):
        return 'External Field: {0}, Angular Frequency: {1}, Phase Shift: {2}, Field Strength: {3}\
        , Dimensions of the Field: {4}'.format(self.name, self.angularFrequency
        , self.phaseShift, self.fieldStrength, self.listOfDimensions)

    def IsParticleInField(self, affectedParticle):
        """ Method determines whether the affected particle is within this field's dimensions

        Args:
            affectedParticle (object: Particle): The particle being affected by the field
        
        Parameters:
            isInFieldValue (float): Value representing whether a particle is
                within the boundaries of the field

        Returns:
            isInFieldValue (float): 1.0 means the particle is within
                boundaries in that dimension. 0.0 means the particle is outside of the field
                boundaries in that dimension.
        """
        # self.listOfDimensions[i][0]: minimum limit
        # self.listOfDimensions[i][1]: maximum limit
        # if both conditions are true, no change is made to isInFieldValue
        # if isInFieldValue is 1.0, field is applied. If isInFieldValue is 0.0, field is not applied
        isInFieldValue = 1.0
        for i in range(3):
            if not (affectedParticle.position[i] > self.listOfDimensions[i][0]
            and affectedParticle.position[i] < self.listOfDimensions[i][1]):
                isInFieldValue = 0.0
        return isInFieldValue
           
    def GenerateField(self, timeElapsed, affectedParticle):
        """Calculates the magntiude of the field in 3D using a cosine function.

        Args:
            timeElapsed (float): Time that has elapsed in the simulation
            affectedParticle (object: Particle): The particle being affected by the field
        
        Returns:
            Strength of Field (ndarray): Strength of the field in three dimensions.
        """
        # calls isParticleInField to determine if the affected particle
        # is within the boundaries of the field. 
        # cosine function will return the amplitude of the field with fieldStrength
        # if angularFrequency is 0.0
        # phaseShift refers to the fraction of a period that the field is shifted by
        return (math.cos(self.angularFrequency * timeElapsed 
        + self.phaseShift * 2 * math.pi) * np.multiply(AbstractExternalFieldClass.IsParticleInField(self, affectedParticle)
        , self.fieldStrength))
