import numpy as np
import math
import scipy.constants as const
from Particle import Particle


class ParticleBunch:
    """This class is to form an object that is made up of other objects, like
    more official than our last "list of bodies" type thing. This way, our
    composition of objects can have properties that can be determined with
    class methods.
    At least. I think so.

    So maybe this is a class where class methods could be used? Not totally sure.
    """

    def __init__(self, numberOfParticles:int=1, bunchPositionSpread=1.0, bunchEnergySpread=0.0
    , bunchMeanEnergy=0.0, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
    , name='Bunch Name'):
        self.numberOfParticles = numberOfParticles
        self.bunchEnergySpread = bunchEnergySpread
        self.bunchMeanEnergy = bunchMeanEnergy
        self.name = name
        self.restMassOfBunch = restMassOfBunch
        self.chargeOfBunch = chargeOfBunch
        self.bunchPositionSpread = bunchPositionSpread

        self.CreateListOfParticles()

    def __repr__(self):
        return 'Name of Particle in bunch: {0}, Bunch of Particles: {1}, Spread of Bunch: {2} \
        , Mean Energy of Bunch: {3}'.format(
        self.name, self.listOfParticles, self.bunchEnergySpread, self.bunchMeanEnergy)
    
    def CreateVelocitySpread(self):
        listOfRandomEnergies = np.random.normal(loc=self.bunchMeanEnergy
        , scale=self.bunchEnergySpread, size=self.numberOfParticles)
        listOfRandomVelocities = [math.sqrt(const.speed_of_light ** 2 
        - (self.restMassOfBunch ** 2 * const.speed_of_light ** 6) 
        / listOfRandomEnergies[i] ** 2) for i in range(self.numberOfParticles)]
        return listOfRandomVelocities
       
    def CreateListOfParticles(self):
        listOfParticles = []
        listOfRandomPositions = np.random.normal(loc=0.0, scale=self.bunchPositionSpread
        , size=3*self.numberOfParticles)
        # really strange, the list of random positions produces an error if the scale
        # is greater than 1e-3, e.g 1e-2 or 1e-1 or 1...
        for i in range(self.numberOfParticles):
            listOfParticles.append(
                Particle(position=np.array([listOfRandomPositions[3*i]
                , listOfRandomPositions[3*i+1], listOfRandomPositions[3*i+2]])
                , velocity=np.array([ParticleBunch.CreateVelocitySpread(self)[i]
                , 0.0, 0.0]), acceleration=np.array([0.0, 0.0, 0.0])
                , restMass=self.restMassOfBunch, charge=self.chargeOfBunch
                , name="%s %s"%(self.name, i+1))
                )
        self.listOfParticles = listOfParticles
        # so as this is self, not initialised with the class, can be called only
        # after this function has been run once. So, make sure to be running this function!

    def UpdateBunchMeanEnergy(self):
        totalEnergy = 0.0
        for i in range(len(self.listOfParticles)):
            totalEnergy += self.listOfParticles[i].TotalEnergy()
        self.bunchMeanEnergy = (totalEnergy / float(len(self.listOfParticles)))

    def UpdateBunchEnergySpread(self):
        # Update the standard deviation of the energy of particles
        # we'll use numpy methods for this.
        spreadArray = np.array([])
        for i in range(len(self.listOfParticles)):
            spreadArray = np.append(spreadArray, self.listOfParticles[i].TotalEnergy())
        self.bunchEnergySpread = np.std(spreadArray)

    def FindBunchMeanVelocity(self):
        totalVelocity = 0.0
        for i in range(len(self.listOfParticles)):
            totalVelocity += self.listOfParticles[i].velocity
        return (totalVelocity / float(len(self.listOfParticles)))


