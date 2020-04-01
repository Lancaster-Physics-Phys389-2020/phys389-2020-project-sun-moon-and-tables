import numpy as np
import math
import scipy.constants as const
from PointMagneticField import PointMagneticFieldClass
from PointElectricField import PointElectricFieldClass

class Particle:
    """Class for generating charged particles that behave relativistcally
    
        Class attributes:
            electricField (object: PointElectricFieldClass): Electric field
                that the particle generates.
            magneticField (object: PointMagneticFieldClass): Magnetic field
                that the particle generates.
            position (numpy array): Current position of the particle
            velocity (numpy array): Current velocity of the particle
            acceleration (numpy array): Current acceleration of the particle
            name (string): Name of the particle
            restMass (float): Rest mass of the particle
            charge (float): Charge of the particle
    """

    #e = 1.6E-19C
    #c = 2.997E8m/s
    e = const.elementary_charge
    c = const.speed_of_light

    
    def __init__(self, position=np.array([0,0,0], dtype=float),
     velocity=np.array([0,0,0], dtype=float), acceleration=np.array([0,0,0],
      dtype=float), name='A Particle', restMass=1.0, charge=const.elementary_charge):
        """ The constructor for Particle Class

            Args:
                position (numpy array): Initial position of the particle
                velocity (numpy array): Initial velocity of the particle
                acceleration (numpy array): Initial acceleration of the particle
                name (string): Name of the particle
                restMass (float): Rest mass of the particle
                charge (float): Charge of the particle
        """
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
        """ Method that returns the rest energy of the particle.

            Returns:
                Rest Energy (float): Energy of the particle when it is stationary
        """
        return (self.restMass * const.speed_of_light * const.speed_of_light)

    def BetaVector(self):
        """ Method that returns Beta (velocity/speed of light) as a vector

            Returns:
                Beta (numpy array): Ratio of the velocity to the speed of light
        """
        return self.velocity / const.speed_of_light

    def LorentzFactor(self):
        """ Method that returns the Lorentz Factor of the particle.

            Returns:
                Lorentz Factor (float): Inverse square root of one minus the 
                    square of the ratio of velocity to the speed of light.
        """
        # Use of abs() and x ** 0.5 provides a more stable calculation of lorentz
        # factor than math.sqrt() at high velocities.
        return 1 / abs( 1 - np.linalg.norm(Particle.BetaVector(self))
         * np.linalg.norm(Particle.BetaVector(self)) ** 0.5)
        
    def RelativisticMass(self):
        """ Method that returns the relativistic mass of the particle

            Returns:
                Relativistic Mass (float): The rest mass of the particle multipled
                    by the Lorentz factor.
        """
        return Particle.LorentzFactor(self) * self.restMass

    def Momentum(self):
        """ Method that returns the relativistic momentum of the particle

            Returns:
                Relativistic Momentum (numpy array): Classical momentum multipled by
                    the Lorentz factor of the particle
        """
        return (np.multiply(Particle.LorentzFactor(self)
        , np.array(self.velocity,dtype=float))* self.restMass)
    
    def TotalEnergy(self):
        """ Method that returns the total energy of the particle

            Returns:
                Total Energy (float): Square root of the sum of the squares of rest 
                    energy and momentum multipled by the speed of light.
        """
        return (math.sqrt((Particle.RestEnergy(self) ** 2)
        + (np.linalg.norm(Particle.Momentum(self)) * const.speed_of_light) ** 2))
    
    def KineticEnergy(self):
        """ Method that returns the kinetic energy of the particle

            Returns:
                Kinetic Energy (float): The total energy minus the rest energy of
                    the particle.
        """
        return Particle.TotalEnergy(self) - Particle.RestEnergy(self)
  
    def UpdateCromer(self, deltaT):
        """ Method that updates the particle's velocity and position with the Euler Cromer method
        
            Args:
                deltaT (float): Time that update lasts for
        """
        self.velocity +=  self.acceleration * deltaT
        self.position +=  self.velocity * deltaT
    
    def UpdateForward(self, deltaT):
        """ Method that updates the particle's velocity and position with the Euler Forward method

            Args:
                deltaT (float): Time that update lasts for
        """
        self.position +=  self.velocity * deltaT
        self.velocity +=  self.acceleration * deltaT
    
    def GenerateElectricField(self, affectedParticle):
        """ Method that returns the electric field from the particle that affects another particle.
            
            Args:
                affectedParticle (object: Particle): The particle being affected by the field
            
            Returns:
                Electric Field (numpy array): The electric field that acts on the affected particle
                    , originating from this particle.
        """
        return self.electricField.GenerateField(affectedParticle)
    
    def GenerateMagneticField(self, affectedParticle):
        """ Method that returns the magnetic field from the particle that affects another particle.
            
            Args:
                affectedParticle (object: Particle): The particle being affected by the field
            
            Returns:
                Magnetic Field (numpy array): The magnetic field that acts on the affected particle
                    , originating from this particle.
        """
        return self.magneticField.GenerateField(affectedParticle)
 