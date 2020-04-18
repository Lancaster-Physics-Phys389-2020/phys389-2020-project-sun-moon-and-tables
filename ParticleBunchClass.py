import numpy as np
import math
import scipy.constants as const
from Particle import Particle


class ParticleBunch:
    """ Generates a collection of Particle objects with a random distribution in energy and position

        Class Attributes:
            listOfParticles (list): List of the particle objects in the bunch
            numberOfParticles (int): The number of particles in the bunch
            bunchPositionSpread (float): The current standard deviation in the 
                positions of the bunch
            bunchEnergySpread (float): The current standard deviation in the energy of
                particles in the bunch
            bunchMeanEnergy (float): The current mean total energy of a particle in the bunch
            restMassOfBunch (float): The rest mass of a particle in the bunch
            bunchPositionMean (float): The initial mean position of the bunch in x, y and z
            name (string): Name of the bunch of particles
    """

    def __init__(self, numberOfParticles:int=1, bunchPositionSpread=1.0, bunchEnergySpread=0.0
    , bunchMeanEnergy=0.0, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
    , bunchPositionMean = 0.0, name='Bunch Name'):
        """ Constructor for the ParticleBunch class. 
                Runs the CreateListOfParticles method upon ParticleBunch initialisation.
            
            Args:
                numberOfParticles (int): The number of particles in the bunch
                bunchPositionSpread (float): The initial standard deviation in the 
                    positions of the bunch
                bunchEnergySpread (float): The initial standard deviation in the energy of
                    particles in the bunch
                bunchMeanEnergy (float): The initial mean total energy of a particle in the bunch
                restMassOfBunch (float): The rest mass of a particle in the bunch
                bunchPositionMean (float): The initial mean position of the bunch in x, y and z
                name (string): Name of the bunch of particles
        """
        self.numberOfParticles = numberOfParticles
        self.bunchEnergySpread = bunchEnergySpread
        self.bunchMeanEnergy = bunchMeanEnergy
        self.name = name
        self.restMassOfBunch = restMassOfBunch
        self.chargeOfBunch = chargeOfBunch
        self.bunchPositionSpread = bunchPositionSpread
        self.bunchPositionMean = bunchPositionMean
        # Instansiates the particle objects and adds them to the attribute: self.listOfParticles
        ParticleBunch.CreateListOfParticles(self)

    def __repr__(self):
        return 'Name of Particle in bunch: {0}, Bunch of Particles: {1}, Spread of Bunch: {2} \
        , Mean Energy of Bunch: {3}'.format(
        self.name, self.listOfParticles, self.bunchEnergySpread, self.bunchMeanEnergy)
    
    def CreateVelocitySpread(self):
        """ Method to convert initial total energy of particles to a starting velocity
                Particles are initialised with parallel trajectories in the x axis.
            
            Parameters: 
                listOfRandomEnergies (list): Normal distribution of energies with mean,
                    standard deviation and size determined by class arguments.
                listOfRandomVelocities (list) : Calculates the velocity corresponding to
                    total energy and rest mass and makes a list of the values.
            Returns:
                listOfRandomVelocities (list): List of random velocities with mean and
                    standard deviation correlated to class arguments of bunchMeanEnergy
                    and bunchEnergySpread
        """
        # create initial energy spread of particles in bunch
        listOfRandomEnergies = np.random.normal(loc=self.bunchMeanEnergy
        , scale=self.bunchEnergySpread, size=self.numberOfParticles)

        # determine velocity of particles in the bunch using their energy
        listOfRandomVelocities = [math.sqrt(const.speed_of_light ** 2 
        - (self.restMassOfBunch ** 2 * const.speed_of_light ** 6) 
        / listOfRandomEnergies[i] ** 2) for i in range(self.numberOfParticles)]

        return listOfRandomVelocities
       
    def CreateListOfParticles(self):
        """ Method to initialise Particle objects and append them to the class attribute
                listOfParticles.
            
            Parameters:
                listOfParticles (list): List of the Particle objects in the bunch
                listOfRandomPositions (list): List of random positions centred about
                    the origin. Standard deviation is determined by class argument.
        """
        listOfParticles = [] # list that will contain particle objects
        # randomly generated initial positions of particles
        listOfRandomPositions = np.random.normal(loc=self.bunchPositionMean, scale=self.bunchPositionSpread
        , size=3*self.numberOfParticles)

        # appends a particle object with a random position in three dimensions, zero acceleration
        # and a parallel velocity in the x direction, no initial velocity in y or z
        # also saves a new name for every particle object
        for i in range(self.numberOfParticles):
            listOfParticles.append(
                Particle(position=np.array([listOfRandomPositions[3*i]
                , listOfRandomPositions[3*i+1], listOfRandomPositions[3*i+2]])
                , velocity=np.array([ParticleBunch.CreateVelocitySpread(self)[i], 0.0, 0.0])
                , acceleration=np.array([0.0, 0.0, 0.0]), restMass=self.restMassOfBunch
                , charge=self.chargeOfBunch, name="%s %s"%(self.name, i+1)))

        # adds listOfParticles as a class attribute
        self.listOfParticles = listOfParticles
        

    def UpdateBunchMeanEnergy(self):
        """ Method to update the bunchMeanEnergy class attribute.

            Parameters:
                totalEnergy (float): Sum of the energy of all particles in the bunch
        """
        totalEnergy = 0.0 # dummy variable

        for i in range(len(self.listOfParticles)):
            totalEnergy += self.listOfParticles[i].TotalEnergy()

        self.bunchMeanEnergy = (totalEnergy / float(len(self.listOfParticles)))

    def UpdateBunchEnergySpread(self):
        """ Method to update the bunchEnergySpread class attribute.
        
            Parameters:
                spreadArray (ndarray): Array of values of the total energy of
                    each particle in the bunch.
        """
        spreadArray = np.array([]) # dummy variable

        for i in range(len(self.listOfParticles)):
            spreadArray = np.append(spreadArray, self.listOfParticles[i].TotalEnergy())

        self.bunchEnergySpread = np.std(spreadArray)

    def FindBunchMeanVelocity(self):
        """ Method to return the mean velocity of the particles in the bunch.

            Parameters: 
                totalVelocity (ndarray): Sum of the velocities of each particle
                    in the bunch
            Returns:
                Mean Velocity of Bunch (ndarray): The sum of all of the velocities
                    of particles in the bunch divided by the number of particles in the
                    bunch.
        """
        totalVelocity = np.array([0.0, 0.0, 0.0], dtype=float) # dummy variable

        for i in range(len(self.listOfParticles)):
            totalVelocity += self.listOfParticles[i].velocity

        return (totalVelocity / float(len(self.listOfParticles)))
    
    def FindBunchMeanPosition(self):
        """ Method to return the mean position of the particles in the bunch.

            Parameters: 
                totalPosition (ndarray): Sum of the velocities of each particle
                    in the bunch
            Returns:
                Mean position of Bunch (ndarray): The sum of all of the positions
                    of particles in the bunch divided by the number of particles in the
                    bunch.
        """
        totalPosition = np.array([0.0, 0.0, 0.0], dtype=float) # dummy variable

        for i in range(len(self.listOfParticles)):
            totalPosition += self.listOfParticles[i].position

        return (totalPosition / float(len(self.listOfParticles)))
    
    def FindBunchMeanAcceleration(self):
        """ Method to return the mean acceleration of the particles in the bunch.

            Parameters: 
                totalAcceleration (ndarray): Sum of the accelerations of each particle
                    in the bunch
            Returns:
                Mean acceleration of Bunch (ndarray): The sum of all of the accelerations
                    of particles in the bunch divided by the number of particles in the
                    bunch.
        """
        totalAcceleration = np.array([0.0, 0.0, 0.0], dtype=float) # dummy variable

        for i in range(len(self.listOfParticles)):
            totalAcceleration += self.listOfParticles[i].acceleration

        return (totalAcceleration / float(len(self.listOfParticles)))

    def FindBunchMeanMomentum(self):
        """ Method to return the mean momentum of the particles in the bunch.

            Parameters: 
                totalMomentum (ndarray): Sum of the momentums of each particle
                    in the bunch
            Returns:
                Mean Momentum of Bunch (ndarray): The sum of all of the momenta
                    of particles in the bunch divided by the number of particles in the
                    bunch.
        """
        totalMomentum = np.array([0.0, 0.0, 0.0], dtype=float) # dummy variable

        for i in range(len(self.listOfParticles)):
            totalMomentum += self.listOfParticles[i].Momentum()
            
        return (totalMomentum / float(len(self.listOfParticles)))



