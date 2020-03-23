import numpy as np 
import math
import scipy.constants as const
from PointElectricField import PointElectricFieldClass
from PointMagneticField import PointMagneticFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle

class EMFieldClass(object):
    """ This class will combine the electric and magnetic fields
    that are within the simulation. This will be a composition
    of electric field classes, much like Particle bunch, but for
    some of these objects, they will be particles and they themselves
    will need to generate electric and magnetic fields by calling
    the pointField class. I need to think about that.
    """
    def __init__(self, bunchOfParticles=ParticleBunch, listOfElectricFields=[ElectricExternalFieldClass]
    , listOfMagneticFields=[MagneticExternalFieldClass], name='Collection of ElectroMagnetic Fields'):
        self.bunchOfParticles = bunchOfParticles
        self.listOfElectricFields = listOfElectricFields
        self.listOfMagneticFields = listOfMagneticFields
        self.name = name
    
    def __repr__(self):
        return 'EM Field Collection: {0}, Constituent Fields: {1}'.format(
        self.name, self.bunchOfParticles + self.listOfElectricFields
        + self.listOfMagneticFields)
    
    def SumOfEMFields(self, affectedParticle:Particle, timeElapsed):
        sumE = np.array([0, 0, 0], dtype=float)
        sumB = np.array([0, 0, 0], dtype=float)
        for i in range(len(self.listOfElectricFields)):
            sumE += self.listOfElectricFields[i].generateField(timeElapsed, affectedParticle)
        for j in range(len(self.listOfMagneticFields)):
            sumB += self.listOfMagneticFields[j].generateField(timeElapsed, affectedParticle)
        for k in range(len(self.bunchOfParticles.listOfParticles)):
            if affectedParticle != self.bunchOfParticles.listOfParticles[k]:
                sumE += self.bunchOfParticles.listOfParticles[k].generateElectricField(affectedParticle)
                sumB += self.bunchOfParticles.listOfParticles[k].generateMagneticField(affectedParticle)
            else:
                pass
        return [sumE, sumB]
        
    def GiveAcceleration(self, particleBunch:ParticleBunch, timeElapsed):
        for i in particleBunch.listOfParticles:
            i.acceleration = ((i.charge * EMFieldClass.SumOfEMFields(self, i, timeElapsed)[0]
            + i.charge * np.cross(i.velocity, EMFieldClass.SumOfEMFields(self, i, timeElapsed)[1]))
            / i.RelativisticMass())


