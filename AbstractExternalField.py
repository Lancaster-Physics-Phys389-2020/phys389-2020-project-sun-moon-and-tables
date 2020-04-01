import numpy as np
import math
import scipy
from GenericField import GenericFieldClass
from abc import ABC, abstractmethod

class AbstractExternalFieldClass(ABC, GenericFieldClass):
    """ Abstract base class for external electromagnetic fields that oscillate sinusoidally

    Class attributes:
            fieldStrength (numpy array): Amplitude of EM field in 3D space
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
                fieldStrength (numpy array): Amplitude of EM field in 3D space
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
            isInFieldArray (numpy array): Truth array representing whether a particle is
                within the boundaries of the field

        Returns:
            isInFieldArray (numpy array): Truth numpy array. 1.0 means the particle is within
                boundaries in that dimension. 0.0 means the particle is outside of the field
                boundaries in that dimension.
        """
        isInFieldArray = np.array([1.0, 1.0, 1.0], dtype=float)
        # self.listOfDimensions[i][0]: minimum limit, self.listOfDimensions[i][1]: maximum limit
        # if both conditions are true, no change is made to isInFieldArray[i]
        for i in range(3):
            if not (affectedParticle.position[i] > self.listOfDimensions[i][0]
            and affectedParticle.position[i] < self.listOfDimensions[i][1]):
                isInFieldArray = np.array([0.0, 0.0, 0.0])
        return isInFieldArray
           
    def GenerateField(self, timeElapsed, affectedParticle):
        """Calculates the magntiude of the field in 3D using a cosine function.

        Args:
            timeElapsed (float): Time that has elapsed in the simulation
            affectedParticle (object: Particle): The particle being affected by the field
        
        Returns:
            Strength of Field (numpy array): Strength of the field in 3D.
        """
        # calls isParticleInField to determine if the affected particle
        # is hit by the electric or magnetic field. multiplies the "truth array"
        # for the dimensions of the field by the time dependence for the field.
        return (math.cos(self.angularFrequency * timeElapsed 
        + self.phaseShift * 2 * math.pi) * np.multiply(AbstractExternalFieldClass.IsParticleInField(self, affectedParticle)
        , self.fieldStrength))
