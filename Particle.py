import numpy as np
import math
import scipy.constants as const


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

    def __repr__(self):
        return 'Particle: {0}, rest Mass: {1:12.3e}, position: {2}, \
        velocity: {3}, acceleration: {4}, charge: {5:12.3e}'.format(
        self.name, self.restMass, self.position,
         self.velocity, self.acceleration, self.charge)

    def BetaVector(self):
        return self.velocity /const.speed_of_light

    def LorentzFactor(self):
        return 1 / (1 - math.sqrt(1 - np.linalg.norm(Particle.BetaVector(self))
        * np.linalg.norm(Particle.BetaVector(self))))

    def Momentum(self):
        return (Particle.LorentzFactor(self) * self.restMass
        * np.array(self.velocity,dtype=float))
    
    def restEnergy(self):
        return (self.restMass * const.speed_of_light * const.speed_of_light)

    def TotalEnergy(self):
        return (math.sqrt((Particle.restEnergy(self) ** 2)
        + (Particle.Momentum(self) * const.speed_of_light) ** 2))
    
    def KineticEnergy(self):
        return Particle.TotalEnergy(self) - Particle.restEnergy(self)
  
    def Update(self, deltaT):
        #Euler forward
        self.position +=  self.velocity*deltaT
        self.velocity +=  self.acceleration*deltaT

 