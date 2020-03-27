import numpy as np
import math
import scipy.constants as const
from PointMagneticField import PointMagneticFieldClass
from PointElectricField import PointElectricFieldClass

class Particle:
    """Regular class. For now.
    I think I can turn each particle into its own class, its
    just that they all follow the same rules, so it feels like
    they don't need to be their own subclasses. Not yet.
    """

    #e = 1.6E-19C
    #c = 2.997E8m/s
    e = const.elementary_charge
    c = const.speed_of_light

    
    def __init__(self, position=np.array([0,0,0], dtype=float),
     velocity=np.array([0,0,0], dtype=float), acceleration=np.array([0,0,0],
      dtype=float), name='A Particle', restMass=1.0, charge=const.elementary_charge):

        self.name = name
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)
        self.restMass = restMass
        self.charge = charge
        self.electricField = PointElectricFieldClass(sourceParticle=self
        , name='Field from %s'%(self.name))
        self.magneticField = PointMagneticFieldClass(sourceParticle=self
        , name='Field from %s'%(self.name))

    def __repr__(self):
        return 'Name: {0}, Rest Mass: {1:12.3e}, Position: {2}, \
        Velocity: {3}, Acceleration: {4}, Charge: {5:12.3e}'.format(
        self.name, self.restMass, self.position
        , self.velocity, self.acceleration, self.charge)

    def RestEnergy(self):
        return (self.restMass * const.speed_of_light * const.speed_of_light)

    def BetaVector(self):
        return self.velocity / const.speed_of_light

    def LorentzFactor(self):
        return 1 / abs( 1 - np.linalg.norm(Particle.BetaVector(self))
         * np.linalg.norm(Particle.BetaVector(self)) ** 0.5)
        # note, by not using math.sqrt, if we end up with beta^2 > 1, this function
        # will not throw an error. We seem to be very close to staying under c,
        # . . . And that seems to have fixed it!
        
    def RelativisticMassVector(self):
        return Particle.LorentzFactor(self) * self.restMass

    def Momentum(self):
        return (Particle.LorentzFactor(self) * self.restMass
        * np.array(self.velocity,dtype=float))
    
    def TotalEnergy(self):
        return (math.sqrt((Particle.RestEnergy(self) ** 2)
        + (np.linalg.norm(Particle.Momentum(self)) * const.speed_of_light) ** 2))
    
    def KineticEnergy(self):
        return Particle.TotalEnergy(self) - Particle.RestEnergy(self)
  
    def Update(self, deltaT):
        #Euler Forward
        self.position +=  self.velocity * deltaT
        self.velocity +=  self.acceleration * deltaT
    
    def Update2(self, deltaT):
        #Euler Cromer
        self.velocity +=  self.acceleration * deltaT
        self.position +=  self.velocity * deltaT
    
    ### This is the section of code where I am trying to get my particles to
    ### generate electromagnetic fields around themselves.
    def GenerateElectricField(self, affectedParticle):
        return self.electricField.GenerateField(affectedParticle)
    # I think we don't need to pass the source of the field as an argument.
    # this particle IS the source of the field. It has all the parameters
    # that it would need to function.
    def GenerateMagneticField(self, affectedParticle):
        return self.magneticField.GenerateField(affectedParticle)
 