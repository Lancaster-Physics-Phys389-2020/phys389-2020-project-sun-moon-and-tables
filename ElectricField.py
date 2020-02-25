from GenericField import AbstractFieldClass
import math as math
import scipy.constants
from ParticleBunchClass import ParticleBunch, Particle
import numpy as np

class ElectricFieldClass(AbstractFieldClass):
    """Class to model just the electric field. Electric field has some properties
    , but for now we are focusing on using the field strength. We'll also need
    to figure out some way of changing its default name so that it is an Electric
    Field
    """
    def __init__(self, electricFieldStrength = np.array([0, 0, 0], dtype = float)
    , name = 'Generic Electric Field'):
        super().__init__(fieldStrength = electricFieldStrength, name = name)
    
    def __repr__(self):
        return 'Electric Field: {0}, Electric Field Strength: {1}'.format(
         self.name, self.fieldStrength)
    
    def GiveAcceleration(self, particleBunch:ParticleBunch):
        #note from ryan: yes, yes you can give a class as an argument for a 
        #function!
        #particleBunch:ParticleBunch states that the argument, particleBunch
        #is actually the ParticleBunch class! Nice.
        for i in particleBunch.listOfParticles:
            i.acceleration = i.charge * self.fieldStrength / i.restMass

