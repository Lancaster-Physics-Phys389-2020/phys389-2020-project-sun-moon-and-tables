import numpy as np 
from AbstractPointField import AbstractPointFieldClass
import scipy.constants as const

class PointElectricFieldClass(AbstractPointFieldClass):
    """ This class will generate an electric field for a point like charged particle.
    Needs it's own generateField method.
    """

    def __init__(self, sourceParticle, name='Electric Point Field'):
        super().__init__(sourceParticle=sourceParticle
        , name=name)

    def __repr__(self):
        return 'Electric Point Field: {0}, Source Particle of Electric Field: {1}'.format(
            self.name, self.sourceParticle)
    
    def generateField(self, affectedParticle):
        displacement = affectedParticle.position - self.sourceParticle.position
        distance = np.linalg.norm(displacement)
        return (const.epsilon_0 / (4 * const.pi)
        * self.sourceParticle.charge * displacement 
        / (distance * distance * distance))