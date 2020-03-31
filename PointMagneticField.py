import numpy as np 
from AbstractPointField import AbstractPointFieldClass
import scipy.constants as const

class PointMagneticFieldClass(AbstractPointFieldClass):
    """ This class will generate a magnetic field for a point like charged particle.
    Needs it's own generateField method.
    """

    def __init__(self, sourceParticle,
    name='Magnetic Point Field'):
        super().__init__(sourceParticle=sourceParticle
        , name=name)

    def __repr__(self):
        return 'Magnetic Point Field: {0}, Source Particle of Magnetic Field: {1}'.format(
            self.name, self.sourceParticle)
    
    def GenerateField(self, affectedParticle):
        displacement = affectedParticle.position - self.sourceParticle.position
        distance = np.linalg.norm(displacement)
        return (const.mu_0 / (4 * const.pi)
        * self.sourceParticle.charge * np.cross(self.sourceParticle.velocity, displacement) 
        / (distance * distance * distance))