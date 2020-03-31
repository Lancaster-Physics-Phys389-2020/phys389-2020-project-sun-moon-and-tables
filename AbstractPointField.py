import numpy as np
from GenericField import GenericFieldClass
from abc import ABC, abstractmethod

class AbstractPointFieldClass(ABC, GenericFieldClass):
    """ This class will have the parameters and functions that all point fields
    will have. They will have to take both the source particle and the affected
    particle as arguments to work out the distance between the two particles.
    """
    
    def __init__(self, sourceParticle,
    name='Abstract Point Field'):
        super().__init__(name=name)
        self.sourceParticle = sourceParticle
        self.name = name
    
    @abstractmethod
    def __repr__(self):
        return 'Point Field: {0}, Source Particle of Field: {1}'.format(
            self.name, self.sourceParticle)
    # as mentioned in the other abstract class, should this be an abstract method?
    # we do intend to overwrite it... so...

    @abstractmethod
    def GenerateField(self):
        pass
    # this makes sense to be an abstract method, as it absolutely has to be overwritten
    # for the electric and magnetic fields, as they are totally different equations.

