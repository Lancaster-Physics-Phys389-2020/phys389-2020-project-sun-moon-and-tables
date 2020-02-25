from GenericField import AbstractFieldClass
import math as math
import scipy.constants
from ParticleBunchClass import ParticleBunch, Particle
import numpy as np

class MagneticFieldClass(AbstractFieldClass):
    """Class to model just the magnetic field.
    """
    def __init__(self, magneticFieldStrength = np.array([0, 0, 0], dtype = float)
    , name = 'Generic Magnetic Field'):
        super().__init__(fieldStrength = magneticFieldStrength, name = name)
    
    def __repr__(self):
        return 'Magnetic Field: {0}, Magnetic Field Strength: {1}'.format(
         self.name, self.fieldStrength)
    
    def GiveAcceleration(self, particleBunch:ParticleBunch):
        #note from ryan: yes, yes you can give a class as an argument for a 
        #function!
        #particleBunch:ParticleBunch states that the argument, particleBunch
        #is actually the ParticleBunch class! Nice.
        for i in particleBunch.listOfParticles:
            i.acceleration = ((i.charge / i.mass)
            * (np.cross(i.velocity, self.fieldStrength)))


