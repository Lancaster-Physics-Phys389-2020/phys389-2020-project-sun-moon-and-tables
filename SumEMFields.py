import numpy as np 
import math
import scipy.constants as const
from PointElectricField import PointElectricFieldClass
from PointMagneticField import PointMagneticFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle

class EMFieldClass:
    """ Class that conatins the external and point-sourced EM fields and combines them to determine acceleration

        Class Attributes:
            bunchOfParticles (object: ParticleBunch): The bunch of particles, where each Particle object produces an EM
                field. 
            listOfElectricFields (list): List of the external electric fields in the simulation
            listOfMagneticFields (list): List of the external magnetic fields in the simulation
            name (string): Name of the collection of electromagnetic fields
    """

    def __init__(self, bunchOfParticles=ParticleBunch, listOfElectricFields=[ElectricExternalFieldClass]
    , listOfMagneticFields=[MagneticExternalFieldClass], name='Collection of ElectroMagnetic Fields'):
        """ Constructor for the EMFieldClass class.
                Args:
                    bunchOfParticles (object: ParticleBunch): The bunch of particles, where each Particle object produces an EM
                        field. 
                    listOfElectricFields (list): List of the external electric fields in the simulation
                    listOfMagneticFields (list): List of the external magnetic fields in the simulation
                    name (string): Name of the collection of electromagnetic fields
        """
        self.bunchOfParticles = bunchOfParticles
        self.listOfElectricFields = listOfElectricFields
        self.listOfMagneticFields = listOfMagneticFields
        self.name = name
    
    def __repr__(self):
        return 'EM Field Collection: {0}, Constituent Fields: {1}'.format(
        self.name, self.bunchOfParticles.listOfParticles + self.listOfElectricFields
        + self.listOfMagneticFields)
    
    def SumOfEMFields(self, affectedParticle:Particle, timeElapsed):
        """ Method to add the contributions of electric and magnetic fields from external sources
                and from other particles in the simulation.
            
            Args:
                affectedParticle (object: Particle): The particle being affected by the
                    electromagnetic fields.
                timeElapsed (float): Time that has elapsed in the simulation
            
            Parameters:
                sumE (ndarray): Stores the sum of the electric field from all other particles and any
                    external fields.
                sumB (ndarray): Stores the sum of the magnetic field from all other particles and any
                    external fields.
            
            Returns:
                [sumE, sumB] (list): List containing the total electric and magnetic fields that are affecting
                    the affectedParticle at timeElapsed in the simulation.
        """
        # adds the external electric fields affecting the particle.
        sumE = sum([self.listOfElectricFields[i].GenerateField(timeElapsed, affectedParticle) 
        for i in range(len(self.listOfElectricFields))])

        # adds the external magnetic fields affecting the particle
        sumB = sum([self.listOfMagneticFields[i].GenerateField(timeElapsed, affectedParticle) 
        for i in range(len(self.listOfMagneticFields))])
        
        # if the source particle of the point EM is not the affected particle by the EM field, the contributing
        # fields are added.
        for k in range(len(self.bunchOfParticles.listOfParticles)):

            if affectedParticle != self.bunchOfParticles.listOfParticles[k]:
                sumE += self.bunchOfParticles.listOfParticles[k].GenerateElectricField(affectedParticle)
                sumB += self.bunchOfParticles.listOfParticles[k].GenerateMagneticField(affectedParticle)

            else:
                pass
        
        return [sumE, sumB]
        
    def GiveAcceleration(self, particleBunch:ParticleBunch, timeElapsed):
        """ Method to update the acceleration of particles in the simulation from the total EM field
                that affects each individual particle.
            
            Args:
                particleBunch (object: ParticleBunch): The bunch of particles that are iterated through
                    to accelerate them all.
                timeElapsed (float): Time that has passed in the simulation so far
        """
        # Lorentz Force acting on each particle, with a field with electric and magnetic components.
        # Force divided by relativistic mass results in acceleration of the particle
        for i in particleBunch.listOfParticles:
            i.acceleration = (np.divide((i.charge * EMFieldClass.SumOfEMFields(self, i, timeElapsed)[0]
            + i.charge * np.cross(i.velocity, EMFieldClass.SumOfEMFields(self, i, timeElapsed)[1]))
            , i.RelativisticMass()))
        