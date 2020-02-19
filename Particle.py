import numpy as np
import math
import copy
import scipy.constants


class Particle:
    """Regular class. For now.
    I think I can turn each particle into its own class, its
    just that they all follow the same rules, so it feels like
    they don't need to be their own subclasses. Not yet.
    """

    #e = 1.6E-19C
    #c = 2.997E8m/s
    e = scipy.constants.elementary_charge
    c = scipy.constants.speed_of_light

    
    def __init__(self, Position=np.array([0,0,0], dtype=float), Velocity=np.array([0,0,0], dtype=float),
    Acceleration=np.array([0,0,0], dtype=float), Name='A Particle', RestMass=1.0, Charge=Particle.e):

        self.name = Name
        self.position = np.array(Position,dtype=float)
        self.velocity = np.array(Velocity,dtype=float)
        self.acceleration = np.array(Acceleration,dtype=float)
        self.restMass = RestMass
        self.charge = Charge

    def __repr__(self):
        return 'Particle: {0}, Rest Mass: {1:12.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}, Charge: {5:12.3e}'.format(
            self.name, self.restMass, self.position, self.velocity, self.acceleration, self.charge)

    def LorentzFactor(self):
        return 1 / (1 - math.sqrt(1 - np.vdot(self.velocity,self.velocity) / (Particle.c * Particle.c)))

    def Momentum(self):
        return Particle.LorentzFactor(self)*self.restMass*np.array(self.velocity,dtype=float)
    
    def RestEnergy(self):
        return (self.restMass * Particle.c * Particle.c)

    def TotalEnergy(self):
        return math.sqrt((Particle.RestEnergy(self) ** 2) + (Particle.Momentum(self)*Particle.c) ** 2)
    
    def KineticEnergy(self):
        return Particle.TotalEnergy(self) - Particle.RestEnergy(self)
  
    def Update(self, deltaT):
        #Euler forward
        self.position +=  self.velocity*deltaT
        self.velocity +=  self.acceleration*deltaT

 