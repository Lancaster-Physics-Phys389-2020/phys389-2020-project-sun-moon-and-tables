from AbstractSimulation import AbstractSimulationClass, np, pd, const, deepcopy
from SumEMFields import EMFieldClass
from ParticleBunchClass import ParticleBunch
from Particle import Particle
import scipy
import math

class SimulationConservationLawsClass(AbstractSimulationClass):
    """ Simulation without external fields that measures conservation of momentum, conservation
            of angular momentum and the total energy of the electromagnetic fields and particles.

        Class Attributes:
            spaceResolution (int): The number of segements each dimension will be split into 
                for the field energy calculation
            inverseResolution (float): Inverse of the number of segments in each dimension to 
                determine where the energy density of the field is to be measured
            listOfPositions (list): List of positions that the field energy density will be measured
            dictionaryOfEnergyDensity (dict): Dictionary of the field energy density at different 
                points in the simulation
            simulationEnergyFields (list): List of the total energy in the electromagnetic fields
                that are tested within the boundaries of the simulation
            simulationEnergyParticles (list): List of the sum total of energy of the particles 
                in the simulation for each timestep
            simulationMomentum (list): List of the sum total momentum of the particles
                in the simulation for each timestep
            simulationAngularMomentum (list): List of the sum total angular momentum of the particles
                in the simulation for each timestep
            simulationTime (list): List of the elapsed time for each timestep of the simulation
            simulationState (list): List of the state of the particles in particleBunch for each timestep
            dummyParticle (object: Particle): The dummy particle that is used to test the field
                at different locations in the simulation.
            totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                fields that interact in the simulation.
            particleBunch (object: ParticleBunch): The bunch of particles that are moved
                throughout the simulation
            duration (float): Duration of the simulation
            largeTimestep (float): The timestep that is throughout the simulation

    """
    def __init__(self, totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=1e-4
    , largeTimestep=1e-6, spaceResolution=10):
        """ Constructor for the SimulationConservationLawsClass class.
                Inherits the __init__ from AbstractSimulationClass.

            Args:
                totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                    fields that interact in the simulation.
                particleBunch (object: ParticleBunch): The bunch of particles that are moved
                    throughout the simulation
                duration (float): Duration of the simulation
                largeTimeStep (float): The timestep that is throughout the simulation
                spaceResolution (int): The number of segements each dimension will be split into 
                    for the field energy calculation
        """
        super().__init__(totalEMField=totalEMField, particleBunch=particleBunch, duration=duration
        , largeTimestep=largeTimestep, smallTimestep=largeTimestep)
        self.spaceResolution = spaceResolution
        self.inverseResolution = 1 / spaceResolution

        self.simulationEnergyFields = []
        self.simulationEnergyParticles = []
        self.simulationMomentum = []
        self.simulationAngularMomentum = []
        self.simulationTime = []
        self.simulationState = []

        # creating the listOfPositions and dictionaryOfEnergyDensity in this way reduces the need
        # to create this list and dictionary from scratch every time these class attributes are called.
        self.listOfPositions = []
        SimulationConservationLawsClass.CreateListOfPositions(self) # creates the list of positions
        self.dictionaryOfEnergyDensity = {}
        SimulationConservationLawsClass.CreateDictionary(self) # creates the dictionary of energies

        # dummyParticle that tests the electric and magnetic field at different points
        # in the simulation.
        self.dummyParticle = Particle(position=np.array([0.0, 0.0, 0.0]), velocity=np.array([0.0, 0.0, 0.0])
        , acceleration=np.array([0.0, 0.0, 0.0]), name="Dummy Particle", restMass=0.0, charge=0.0)
        

    def CreateListOfPositions(self):
        """ Updates the listOfPositions class attribute to add a list of positions that 
                the field will be tested at by the dummyParticle.

            Parameters:
                listOfPositions (list): List of positions that the dummy particle
                    will be moved through
                distanceBetweenPositions (float): Parameter that is used to determine
                    the distance between testing locations that is a function of the 
                    spread of the particleBunch.
        """
        listOfPositions = []
        # distanceBetweenPositions is a function of the resolution that the field
        # is being tested with (inverseResolution) and covers a total distance 10 times
        # greater than the initial bunchPositionSpread.
        distanceBetweenPositions = (
        self.inverseResolution * self.particleBunch.bunchPositionSpread * 10)

        for i in range(self.spaceResolution + 1):
            for j in range(self.spaceResolution + 1):
                for k in range(self.spaceResolution + 1):
                    
                    # list of positions is rounded to 5dp to remove floating point errors and allows
                    # for small scale simulations with very small distances.
                    listOfPositions.append(np.round(np.array(
                    [distanceBetweenPositions * i, distanceBetweenPositions * j, distanceBetweenPositions * k] 
                    , dtype=float), decimals=5))

        self.listOfPositions = listOfPositions
    
    def CreateDictionary(self):
        """ Updates the dictionaryOfEnergyDensity class attribute to form a dictionary
                of positions with keys that match to the energy density at the current
                timestep.
            
            Parameters:
                dictionary (dictionary): A dictionary that is created with the positions
                    of field testing with keys as tuples.
        """
        dictionary = {} # dummy variable

        # dictionary with keys relating to the positions in the simulation that
        # energy density will be measured
        # dictionary is initially empty
        for i in self.listOfPositions:
            dictionary.update({tuple(i.tolist()) : None })
        
        self.dictionaryOfEnergyDensity = dictionary
    
    def EnergyDensity(self, timeElapsed):
        """ Returns the total energy density at a position in the simulation.

            Args:
                timeElapsed (float): Time that has elapsed in the current simulation

            Parameters:
                electromagneticFields (list): The electric and magnetic fields calculated at
                    the current position of the dummy particle
                energyDensityElectricFields (float): Half of vacuum permittivity multipled by
                    the dot product of the electric field
                energyDensityMagneticFields (float): Half of vacuum permeability multipled by
                    the dot product of the magnetic field

            Returns:
                Total of energy density from electromagnetic fields (float): Adds the magnetic and
                    elecric field components of energy
        """
        electromagneticFields = self.totalEMField.SumOfEMFields(self.dummyParticle, timeElapsed)

        energyDensityElectricFields = (const.epsilon_0 / 2) * np.dot(electromagneticFields[0]
        , electromagneticFields[0])

        energyDensityMagneticFields = (const.mu_0 / 2) * np.dot(electromagneticFields[1]
        , electromagneticFields[1])

        return energyDensityElectricFields + energyDensityMagneticFields
        
    def DictionaryOfEnergyDensity(self, timeElapsed):
        """ Updates the value corresponding to each key (a position in the simulation) with the energy
                density at that point.
            
            Args:
                timeElapsed (float): Time that has elapsed in the current simulation
        """
         # update the value for each key in the dictionary with the new energy density
        for i in self.listOfPositions:
            self.dummyParticle.position = i
            self.dictionaryOfEnergyDensity[tuple(i.tolist())] = SimulationConservationLawsClass.EnergyDensity(self, timeElapsed=timeElapsed)

    def IntegrateEnergyDensity(self, timeElapsed):
        """ Performs a modified Rienmann Sum in three dimensions to integrate the energy density 
                from the electric and magnetic fields from the particles. The total volume of the simulation
                is separated into small cubes with eight corners each. The mean energy density of each of the
                eight corners for each cube is calculated and multiplied by the volume of that cube.

            Args:
                timeElapsed (float): Time that has elapsed in the current simulation
            
            Parameters:
                distance (float): Equal to distanceBetweenPositions in CreateListOfPositions(self). The distance
                    between points in the simulation that will be tested.
                integralOfEnergy (float): The resulting integral of energy density with respect to volume
                mean (float): The mean energy density across the eight points of each cube
            
            Returns:
                integralOfEnergy (float): The resulting sum of the integrals of energy contained in the 
                    electromagnetic fields at each timestep in the simulation.
        """
        SimulationConservationLawsClass.DictionaryOfEnergyDensity(self, timeElapsed=timeElapsed) # update the saved energies

        # distance between points that are inspected in the simulation space
        distance = self.inverseResolution * self.particleBunch.bunchPositionSpread * 10
        integralOfEnergy = 0.0 # dummy variable

        # This iterates through all of the cubes in the simulation space. As it uses i and i+1 to reference
        # each pair of parallel points in a cube, the range stops after spaceResolution * distance rather
        # than (spaceResolution + 1) * distance, like in CreateListOfPositions. 
        for i in np.arange(start=0.0, stop=round(distance * self.spaceResolution, ndigits=5), step=round(distance, ndigits=5)):
            for j in np.arange(start=0.0, stop=distance * self.spaceResolution, step=round(distance, ndigits=5)):
                for k in np.arange(start=0.0, stop=distance * self.spaceResolution, step=round(distance, ndigits=5)):
                    
                    # determine the mean energy density for each cube using its corners
                    # floating point errors are common here, so every value must be rounded to 5dp
                    # without the round statements, expressions look like:
                    # self.dictionaryOfEnergyDensity[(i+distance,j,k)]
                    mean = (self.dictionaryOfEnergyDensity[(round(i, ndigits=5),round(j, ndigits=5),round(k, ndigits=5))] 
                    + self.dictionaryOfEnergyDensity[(round(i+distance, ndigits=5),round(j, ndigits=5),round(k, ndigits=5))]
                    + self.dictionaryOfEnergyDensity[(round(i, ndigits=5),round(j+distance, ndigits=5),round(k, ndigits=5))] 
                    + self.dictionaryOfEnergyDensity[(round(i+distance, ndigits=5),round(j+distance, ndigits=5),round(k, ndigits=5))]
                    + self.dictionaryOfEnergyDensity[(round( i, ndigits=5),round(j, ndigits=5),round(k+distance, ndigits=5))] 
                    + self.dictionaryOfEnergyDensity[(round(i+distance, ndigits=5),round(j, ndigits=5),round(k+distance, ndigits=5))]
                    + self.dictionaryOfEnergyDensity[(round(i, ndigits=5),round(j+distance, ndigits=5),round(k+distance, ndigits=5))] 
                    + self.dictionaryOfEnergyDensity[(round(i+distance, ndigits=5),round(j+distance, ndigits=5),round(k+distance, ndigits=5))]
                    / float(8))

                    integralOfEnergy += mean * (distance*distance*distance)
        return integralOfEnergy
        

    def RunSimulation(self):
        """ Method that runs the simulation that tests conservation laws.

            Parameters:
                timeElapsed (float): Time that has elapsed in the current simulation
                timeStep (float): Equal to largeTimeStep
                particlesOutOfBounds (int): The number of particles in the simulation that
                    are out of the boundaries of the testing fields
                simulationMomentum (float): Norm of the sum of linear momentum of particles
                    in the simulation
                simulationAngularMomentum (float): Norm of the sum of the angular momentum of
                    the particles in the simulation, which is the cross product of each particle's
                    position and linear momentum
                simulationEnergyFields (float): Energy of the simulation that is stored in the fields
                simulationEnergyParticles (float): Energy of the simulation that is stored in the
                    kinetic energy of the particles, the total energy minus the rest energy
        """
        # stops the simulation if external fields are added
        if (len(self.totalEMField.listOfElectricFields) != 0 or
        len(self.totalEMField.listOfMagneticFields) != 0):
            print("Remove any external fields from this simulation in order to continue.")
            return None

        timeElapsed = 0.0
        timestep = self.largeTimestep # only the largeTimestep is used in this simulation

        # number of particles that are out of bounds of the simulation. If greater than 0
        # the simulation is stopped
        # this is because only a small volume of space can be tested to measure EM field energy
        # and this result is inaccurate if particles leave the simulation space
        particlesOutOfBounds = 0  
        
        while timeElapsed < self.duration:

            for i in range(self.particleBunch.numberOfParticles):
                for j in range(3):
                    # if any of the components of a particle's position fall outside of the boundaries of 
                    # how far the electromagnetic field energy is tested, the simulation is ended. 
                    if (self.particleBunch.listOfParticles[i].position[j] < 0.0 or 
                    self.particleBunch.listOfParticles[i].position[j] > 10 * self.particleBunch.bunchPositionSpread):
                        particlesOutOfBounds += 1
                        
            if particlesOutOfBounds < 0:
                print("The simulation was halted after %s secs as particles escaped the testing volume\n\
                and the calculation of energy from fields became inaccurate."
                %(timeElapsed))
                break

            self.simulationTime.append(deepcopy(timeElapsed)) # save elapsed time
            self.simulationState.append(deepcopy(self.particleBunch.listOfParticles)) # save state of all particles

            # save total momentum of all particles
            simulationMomentum = np.linalg.norm(sum([self.particleBunch.listOfParticles[i].Momentum() 
            for i in range(self.particleBunch.numberOfParticles)]))
            self.simulationMomentum.append(deepcopy(simulationMomentum)) 

            # save total angular momentum of all particle
            simulationAngularMomentum = np.linalg.norm(sum([np.cross(
            self.particleBunch.listOfParticles[i].position, self.particleBunch.listOfParticles[i].Momentum()) 
            for i in range(self.particleBunch.numberOfParticles)]))
            self.simulationAngularMomentum.append(deepcopy(simulationAngularMomentum)) 

            # save total potential energy in electromagnetic fields in the simulation space
            simulationEnergyFields = SimulationConservationLawsClass.IntegrateEnergyDensity(self, timeElapsed=timeElapsed)
            self.simulationEnergyFields.append(deepcopy(simulationEnergyFields))

            # save total kinetic energy of all particles
            simulationEnergyParticles = sum([self.particleBunch.listOfParticles[i].KineticEnergy() for i in 
            range(self.particleBunch.numberOfParticles)])
            self.simulationEnergyParticles.append(deepcopy(simulationEnergyParticles))
            
            # give all particles correct acceleration by determining the total electric
            # and magnetic fields that act on the particles
            self.totalEMField.GiveAcceleration(self.particleBunch, timeElapsed)

            # apply the euler cromer method to update the velocity and position of all particles
            for i in range(len(self.particleBunch.listOfParticles)):
                self.particleBunch.listOfParticles[i].UpdateCromer(timestep)

            timeElapsed += timestep

    def SaveSimulation(self, fileName):
        """ Method to save the simulation data to a .pkl file as a pandas dataframe

            Args:
                fileName (string): Name of the saved data file
            
            Parameters:
                dictionary (dictionary): Dictionary that contains data for the elapsed time, total
                    energy of the particles and fields in the simulation, the total momentum of particles
                    in the simulation and the total angular momentum of particles in the simulation.
                dataFrame (pandas dataframe): Dataframe of dictionary
        """
        dictionary = {'Time':self.simulationTime, 'Simulation':self.simulationState
        , 'EnergyFields':self.simulationEnergyFields, 'Momentum':self.simulationMomentum
        , 'AngularMomentum': self.simulationAngularMomentum
        , 'EnergyParticles':self.simulationEnergyParticles}

        dataFrame = pd.DataFrame(dictionary)
        dataFrame.to_pickle("%s.pkl"%(fileName))
        