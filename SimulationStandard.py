from AbstractSimulation import AbstractSimulationClass, np, pd, deepcopy, stats
from SumEMFields import EMFieldClass
from ParticleBunchClass import ParticleBunch
import scipy.constants as const



class SimulationStandardClass(AbstractSimulationClass):
    """ Class that compares the result of altering the phase of accelerating electric fields in a cyclotron.

        Class Attributes:
            simulateState (list): List of the state of the particles in particleBunch for each timestep
            simulationEnergy (list): List of the mean energy of the particles in the simulation for each
                timestep
            simulationSpread (list): List of the standard deviation in the energy of particles in the
                simulation for each timestep
            simulationTime (list): List of the elapsed time for each timestep of the simulation
            totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                fields that interact in the simulation.
            particleBunch (object: ParticleBunch): The bunch of particles that are moved
                throughout the simulation
            duration (float): Duration of the simulation
            largeTimeStep (float): The timestep that is used when on average, the bunch is
                outside of the accelerating electric field
            smallTimeStep (float): The shorter timestep that is used when on average, the
                bunch is inside of the accelerating electric field.
    """

    def __init__(self, totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=1.0
    , largeTimestep=1e-3, smallTimestep=1e-8):
        """ Constructor for the SimulationStandardClass class.
                Inherits the __init__ from AbstractSimulationClass.
            
            Args:
                totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                    fields that interact in the simulation.
                particleBunch (object: ParticleBunch): The bunch of particles that are moved
                    throughout the simulation
                duration (float): Duration of the simulation
                largeTimeStep (float): The timestep that is used when on average, the bunch is
                    outside of the accelerating electric field
                smallTimeStep (float): The shorter timestep that is used when on average, the
                    bunch is inside of the accelerating electric field.
        """
        super().__init__(totalEMField=totalEMField, particleBunch=particleBunch, duration=duration
        , largeTimestep=largeTimestep, smallTimestep=smallTimestep)
        
        self.simulationState = [] # position, velocity, acceleration data
        self.simulationEnergy = [] # mean of enery of particles in simulation
        self.simulationSpread = [] # std deviation of energy of particles in simulation
        self.simulationTime = [] # time of simulation (x axis)

    def RunSimulation(self):
        """Method that runs the standard simulation.

            Paramaters:
                timeElapsed (float): Time that has elapsed in the current simulation
                timeStep (float): Either refers to smallTimeStep or largeTimeStep depending on the mean
                    x position of particles in the simulation.
                acceleratingFieldDimensions (list): Dimensions of the first phase changing field.
                testIfVelocityTooHigh (numpy array): numpy array that holds the expected value for the
                    updated velocity if the current timestep is used
                numberOfTimesBreakIsPrevented (int): The number of times that the emergency shortended 
                    timestep was used in a row to prevent a crash
        """
        timeElapsed = 0.0
    
        while timeElapsed < self.duration:
            timestep = self.largeTimestep
            meanXPosition = stats.mean([self.particleBunch.listOfParticles[i].position[0] 
            for i in range(self.particleBunch.numberOfParticles)])
            acceleratingFieldDimensions = self.totalEMField.listOfElectricFields[0].listOfDimensions[0]
            # It is assumed that the acceleratingFieldDimensions is similar to the dimensions 
            # of other accelerating electric fields.
            # If these dimensions differ greatly, the time-steps of the simulation will not be
            # adjusted accurately.
            if (meanXPosition < acceleratingFieldDimensions[1] and
            meanXPosition > acceleratingFieldDimensions[0]):
                timestep = self.smallTimestep
                # if the particles are inside of the accelerating field, the simulation runs slower
            self.simulationState.append(deepcopy(self.particleBunch.listOfParticles))
            self.simulationEnergy.append(deepcopy(self.particleBunch.bunchMeanEnergy))
            self.simulationSpread.append(deepcopy(self.particleBunch.bunchEnergySpread))
            self.simulationTime.append(deepcopy(timeElapsed))

            self.totalEMField.GiveAcceleration(self.particleBunch, timeElapsed)
            self.particleBunch.UpdateBunchMeanEnergy(), self.particleBunch.UpdateBunchEnergySpread()
            
            numberOfTimesBreakIsPrevented = 0
            while True:
                testIfVelocityTooHigh = (self.particleBunch.FindBunchMeanVelocity() 
                + self.particleBunch.FindBunchMeanAcceleration() * timestep)
                if np.linalg.norm(testIfVelocityTooHigh) < const.speed_of_light:
                    break
                else:
                    timestep = 0.1 * timestep
                    numberOfTimesBreakIsPrevented += 1
            
            for i in range(len(self.particleBunch.listOfParticles)):
                self.particleBunch.listOfParticles[i].UpdateCromer(timestep)
            if numberOfTimesBreakIsPrevented==5:
                break
                # if the timestep needed to be made 1e5 times smaller in order to move the simulation
                # forward another timestep, then the simulation should stop and save instead of generating
                # corrupted data.
            timeElapsed += timestep

    
    def SaveSimulation(self, fileName):
        """ Method to save the simulation data to a .pkl file as a pandas dataframe

            Args:
                fileName (string): Name of the saved data file
            
            Parameters:
                dictionary (dictionary): Dictionary that contains data for the elapsed time, state
                    of the bunch in the simulation, mean particle energy and standard deviation
                    of particle energy for each timestep in the simulation.
                dataFrame (pandas dataframe): Dataframe of dictionary
        """
        dictionary = {'Time':self.simulationTime, 'Simulation':self.simulationState
        , 'Energy':self.simulationEnergy, 'Spread':self.simulationSpread}
        dataFrame = pd.DataFrame(dictionary)
        dataFrame.to_pickle("%s.pkl"%(fileName))