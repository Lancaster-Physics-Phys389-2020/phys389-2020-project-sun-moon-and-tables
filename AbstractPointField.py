import numpy as np
from GenericField import GenericFieldClass
from abc import ABC, abstractmethod

class AbstractPointFieldClass(ABC, GenericFieldClass):
    """ Abstract base class for electromagnetic fields originating from point sources

        Class Attributes:
            sourceParticle (object: Particle): The source particle that generates the
                EM field
            name (string): Name of the point source EM field
    """
    
    def __init__(self, sourceParticle,name='Abstract Point Field'):
        """ Constructor for any point sourced EM field. Inherits the __init__ from GenericFieldClass

            Args:
                sourceParticle (object: Particle): The source particle that generates the
                    EM field
                name (string): Name of the point source EM field
        """
        super().__init__(name=name)
        self.sourceParticle = sourceParticle
        self.name = name
    
    @abstractmethod
    def __repr__(self):
        return 'Point Field: {0}, Source Particle of Field: {1}'.format(
            self.name, self.sourceParticle)
    
    @abstractmethod
    def GenerateField(self):
        """ Abstract method for generating either electric or magnetic fields.
                Method is abstract since electric and magnetic fields are generated very
                differently.
        """
        pass
    
