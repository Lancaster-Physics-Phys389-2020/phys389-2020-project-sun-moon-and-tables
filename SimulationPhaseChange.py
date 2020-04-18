from AbstractSimulation import AbstractSimulationClass, np, pd, deepcopy, const
from SumEMFields import EMFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from ParticleBunchClass import ParticleBunch

class SimulationPhaseChangeClass(AbstractSimulationClass):
    """ Class that compares the result of altering the phase of accelerating electric fields in a cyclotron.

        Class Attributes:
            listOfPhaseChangingFields (list): List of fields that will have their phase changed across
                different simulations. Members of list should be a subset of the totalEMField attribute.
            phaseResolution (int): Number of segements that the total phase shift that can be applied to a
                sinusoidal function (2*pi) will be split into.
            simulationFinalSpread (list): List of the final standard deviation in the energy of particles
                in the simulation at the end of each simulation.
            simulationPhaseShift (list): List of the phase shift applied in each simulation.
            totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                fields that interact in the simulation.
            particleBunch (object: ParticleBunch): The bunch of particles that are moved
                throughout the simulation
            duration (float): Duration of each simulation
            largeTimeStep (float): The timestep that is used when on average, the bunch is
                outside of the accelerating electric field
            smallTimeStep (float): The shorter timestep that is used when on average, the
                bunch is inside of the accelerating electric field.
    """

    def __init__(self, listOfPhaseChangingFields=[ElectricExternalFieldClass], phaseResolution:int=50
    , totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=0.1, largeTimestep=1e-3
    , smallTimestep=1e-8):
        """ Constructor for the SimulationPhaseChangeClass class.
                Inherits the __init__ from AbstractSimulationClass.
            
            Args:
                listOfPhaseChangingFields (list): List of fields that will have their phase changed across
                    different simulations. Members of list should be a subset of the totalEMField attribute.
                phaseResolution (int): Number of segements that the total phase shift that can be applied to a
                    sinusoidal function (2*pi) will be split into.
                totalEMField (object: EMFieldClass): The combined collection of electromagnetic
                    fields that interact in the simulation.
                particleBunch (object: ParticleBunch): The bunch of particles that are moved
                    throughout the simulation
                duration (float): Duration of each simulation
                largeTimeStep (float): The timestep that is used when on average, the bunch is
                    outside of the accelerating electric field
                smallTimeStep (float): The shorter timestep that is used when on average, the
                    bunch is inside of the accelerating electric field.
        """
        super().__init__(totalEMField=totalEMField, particleBunch=particleBunch, duration=duration
        , largeTimestep=largeTimestep, smallTimestep=smallTimestep)
        self.listOfPhaseChangingFields = listOfPhaseChangingFields
        self.phaseResolution = phaseResolution
        self.simulationFinalSpread = [] # y axis data
        self.simulationPhaseShift = [] # x axis data

    def RunSimulation(self):
        """Method that runs the series of simulations that determine the impact of altering phase shift.

            Paramaters:
                initialListOfParticles (list): Deepcopy of the initial conditions of the first simulation,
                    so that these can be re-created for following simulations.
                timeElapsed (float): Time that has elapsed in the current simulation
                timeStep (float): Either refers to smallTimeStep or largeTimeStep depending on the mean
                    x position of particles in the simulation.
                acceleratingFieldDimensions (list): Dimensions of the first phase changing field.
        """
        #creates a copy of the initial state of the system
        initialListOfParticles = deepcopy(self.particleBunch.listOfParticles)

        # Runs a new simulation each time this for loop is iterated
        for j in range(self.phaseResolution): 
            
            # shifts all phase shifted fields for the next simulation
            SimulationPhaseChangeClass.CreatePhaseShiftedFields(self, j)

            timeElapsed = 0.0
    
            while timeElapsed < self.duration:
                timestep = self.largeTimestep

                # this simulation accelerates a bunch of particles about the x-z plane, starting at
                # 0.0, 0.0, 0.0 . As a result, the x position of the bunch is useful at informing 
                # where accelerating electric fields will be.
                meanXPosition = (sum([self.particleBunch.listOfParticles[i].position[0] 
                for i in range(self.particleBunch.numberOfParticles)]) 
                / float(self.particleBunch.numberOfParticles))

                # It is assumed that the acceleratingFieldDimensions is similar to the dimensions 
                # of other accelerating electric fields.
                # If these dimensions differ greatly, the time-steps of the simulation will not be
                # adjusted accurately.
                acceleratingFieldDimensions = self.listOfPhaseChangingFields[0].listOfDimensions[0]
                
                # if the particles are inside of the accelerating field, the simulation runs slower
                if (meanXPosition < acceleratingFieldDimensions[1] and 
                meanXPosition > acceleratingFieldDimensions[0]):
                    timestep = self.smallTimestep
                   
                # give all particles correct acceleration by determining the total electric
                # and magnetic fields that act on the particles
                self.totalEMField.GiveAcceleration(self.particleBunch, timeElapsed)
                # update the mean energy and std. dev. in energy of the bunch with the current values
                self.particleBunch.UpdateBunchMeanEnergy(), self.particleBunch.UpdateBunchEnergySpread()

                # the following prevents a timestep that is too large causing a particle to move faster than the
                # speed of light
                # therefore, this check comes after updating acceleration but before applying the euler cromer
                # method
                numberOfTimesBreakIsPrevented = 0

                while True:

                    testIfVelocityTooHigh = (self.particleBunch.FindBunchMeanVelocity() 
                    + self.particleBunch.FindBunchMeanAcceleration() * timestep)

                    # if the velocity is lower than the speed of light, continue
                    if np.linalg.norm(testIfVelocityTooHigh) < const.speed_of_light:
                        break

                    else:
                        # make the timestep 10 times smaller and try again
                        timestep = 0.1 * timestep
                        numberOfTimesBreakIsPrevented += 1

                # apply the euler cromer method to update the velocity and position of all particles                
                for i in range(self.particleBunch.numberOfParticles):
                    self.particleBunch.listOfParticles[i].UpdateCromer(timestep)
                
                # if the timestep needed to be made 1e5 times smaller in order to move the simulation
                # forward another timestep, then the simulation should stop and save instead of generating
                # corrupted data.
                if numberOfTimesBreakIsPrevented == 5:
                    print("The simulation was halted after %s secs as relativistic effects began to break down."
                    %(timeElapsed))
                    break
                timeElapsed += timestep

            # save the final energy spread of the bunch
            self.simulationFinalSpread.append(deepcopy(self.particleBunch.bunchEnergySpread))
            # save the phase shift of the first alternating electromagnetic field
            # all phase changing fields have the same phase shift in any simulation
            self.simulationPhaseShift.append(deepcopy(self.listOfPhaseChangingFields[0].phaseShift))

            # at the end of each simulation, the initial particle state is restored
            self.particleBunch.listOfParticles = deepcopy(initialListOfParticles)
            print(j+1, "simulations completed")

        # at the end of all the simulations, the first value is added to the end.
        # This ensures the radial graph forms a complete circle
        self.simulationFinalSpread.append(deepcopy(self.simulationFinalSpread[0]))
        self.simulationPhaseShift.append(deepcopy(self.simulationPhaseShift[0]+1.0))
        
    def CreatePhaseShiftedFields(self, iterationOfSimulation:int):
        """ Method to shift the phase of fields in listOfPhaseChangingFields

            Args:
                iterationOfSimulation (int): The number of simulations that have been completed
            
            Parameters:
                inverseOfSimulation (float): Inverse of the number of simulations that will be run, which
                    determines what fraction the phase will be shifted in each iteration
        """
        inverseOfResolution = 1 / self.phaseResolution
        # starts at smallest phase shift and ends at a full period phase shift
        for i in self.listOfPhaseChangingFields:
            i.phaseShift = np.round(inverseOfResolution + inverseOfResolution * iterationOfSimulation, decimals = 5)
    
    def SaveSimulation(self, fileName):
        """ Method to save the simulation data to a .pkl file as a pandas dataframe

            Args:
                fileName (string): Name of the saved data file
            
            Parameters:
                dictionary (dictionary): Dictionary that contains phase shift data and the final standard deviation
                    of energies of particles in each simulation
                dataFrame (pandas dataframe): Dataframe of dictionary
        """
        dictionary = {'Phase':self.simulationPhaseShift, 'FinalSpread':self.simulationFinalSpread}

        dataFrame = pd.DataFrame(dictionary)
        dataFrame.to_pickle("%s.pkl"%(fileName))