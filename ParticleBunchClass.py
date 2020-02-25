from numpy import np
from Particle import Particle


class ParticleBunch(object):
    """This class is to form an object that is made up of other objects, like
    more official than our last "list of bodies" type thing. This way, our
    composition of objects can have properties that can be determined with
    class methods.
    At least. I think so.

    So maybe this is a class where class methods could be used? Not totally sure.
    """

    def __init__(self, listOfParticles = [], bunchSpread = 0.0
     , bunchMeanEnergy = 0.0, name = 'Bunch Name'):
        self.listOfParticles = listOfParticles
        self.bunchSpread = bunchSpread
        self.bunchMeanEnergy = bunchMeanEnergy
        self.name = name

    def __repr__(self):
        return 'Name of Bunch: {0}, Bunch of Particles: {1}, Spread of Bunch: {2} \
        , Mean Energy of Bunch: {3}'.format(self.name, self.listOfParticles
        , self.bunchSpread, self.bunchMeanEnergy)
        
    def FindBunchSpread(self):
        pass
    
    def FindBunchMeanEnergy(self):
        pass

