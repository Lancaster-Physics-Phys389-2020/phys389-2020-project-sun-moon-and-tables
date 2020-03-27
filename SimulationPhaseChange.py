from AbstractSimulation import AbstractSimulationClass, np, pd, deepcopy, stats
from SumEMFields import EMFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from ParticleBunchClass import ParticleBunch
# this also allows us to import all the modules used, which is helpful.

# okay, so we want a file for runSimulation. 
# that has separate saving methods and things like that.
# so it makes sense to have them as separate classes.
# this file is to serve as the "main.py" equivalent for running the 
# changing phase simulation, where we run the simulation with
# a different accelerating field with different phases.
# the main.py file will actually contain the defining of the different
# bunches of particles etc.
# but this will contain all the methods for running the changing phase simulation
# and the specific saving required for that.
# bear in mind, you may need to think about how the data is saved and loaded
# for the plots in the PlottingClass.

class SimulationPhaseChangeClass(AbstractSimulationClass):
    """ This class is responsible for containing methods that create
    a simulation that allows the comparison of different phase shifts 
    in external accelerating electric fields in order to find the phase shift
    that reduces bunch energy spread the most.
    """
    def __init__(self, listOfPhaseChangingFields=[ElectricExternalFieldClass], phaseResolution=50
    , totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=0.1, largeTimestep=1e-3
    , smallTimestep=1e-8):
        super().__init__(totalEMField=totalEMField, particleBunch=particleBunch, duration=duration
        , largeTimestep=largeTimestep, smallTimestep=smallTimestep)
        self.listOfPhaseChangingFields = listOfPhaseChangingFields
        self.phaseResolution = phaseResolution
        self.simulationFinalSpread = [] # our y axis data
        self.simulationPhaseShift = [] # our x axis data

    def RunSimulation(self):
        """This method runs the simulation. As it is an abstract
        method, it is required in order for this class to operate.
        """
        simulationFinalSpread = [] # our y axis data
        simulationPhaseShift = [] # our x axis data
        initialListOfParticles = []
        initialListOfParticles = deepcopy(self.particleBunch.listOfParticles) 
        #creates a copy of the initial state of the system
        
        SimulationPhaseChangeClass.IdentifyChangingFields(self)
        # identifies the changing fields in the totalEMField object
        # by running this, I should be able to update the listOfPhaseChangingFields,
        # and this will alter the electric fields inside of totalEMField
        # and once this is run, we can save the phase shift of simulation with 
        # self.listOfPhaseChangingFields
        for j in range(self.phaseResolution): #central for loop for the simulations.
            # each time this is run, a new simulation is run. the final energy spread for 
            # that simulation is then saved.
            SimulationPhaseChangeClass.CreatePhaseShiftedFields(self, j)

            timeElapsed = 0.0
    
            while timeElapsed < self.duration:
                timestep = self.largeTimestep
                meanXPosition = stats.mean([self.particleBunch.listOfParticles[i].position[0] 
                for i in range(self.particleBunch.numberOfParticles)])
                if (meanXPosition < 0.5 and meanXPosition > -0.5):
                    timestep = self.smallTimestep
                # so here we are just using the first proton to give a determination of position for the timestep
                # and it really seems to work. 
                # deepcopy is required to make sure that the "append problem" 
                # is not realised
                self.totalEMField.GiveAcceleration(self.particleBunch, timeElapsed)
                self.particleBunch.UpdateBunchMeanEnergy(), self.particleBunch.UpdateBunchEnergySpread()
                for i in range(len(self.particleBunch.listOfParticles)):
                    self.particleBunch.listOfParticles[i].Update(timestep)
                timeElapsed += timestep

            self.simulationFinalSpread.append(deepcopy(self.particleBunch.bunchSpread))
            self.simulationPhaseShift.append(deepcopy(self.listOfPhaseChangingFields[0].phaseShift))
            self.particleBunch.listOfParticles = deepcopy(initialListOfParticles)
            # this restores the state of the particles in the simulation to their initial state
            # this is not needed for the fields as they are simply queried at the timeElapsed
        self.simulationFinalSpread.append(self.simulationFinalSpread[0])
        self.simulationPhaseShift.append(self.simulationPhaseShift[0]+1.0)
        # at the end of the simulation, the first value is stuck to the end, to ensure the graph 

    def IdentifyChangingFields(self):
        """method to identify which of the fields inside of 
        the EMFieldClass object are having their phase changed 
        in this simulation
        """
        if len(self.listOfPhaseChangingFields) == 0:
            raise ValueError("You have not entered any fields that you will change\
                the phase of for this simulation that determines the affect of \
                    changing the phase of field.")
        for i in range(len(self.listOfPhaseChangingFields)):
            for j in range(len(self.totalEMField.listOfElectricFields)):
                if self.listOfPhaseChangingFields[i] == self.totalEMField.listOfElectricFields[j]:
                    self.listOfPhaseChangingFields[i] = self.totalEMField.listOfElectricFields[j]
                    # determines if a phase changing field is in the total list of electric fields
                    # if it is, changes the reference for that phase changing field to be the reference
                    # for the already existing electric field object that is being used by the totalEMField
                    # class. This way, changes can be made to listOfPhaseChangingFields[i] that affect the state
                    # of totalEMFields.

                    # doing it in this way also ensures that this check need only be made once,
                    # rather than doing it every single time the RunSimulation for loop runs.
    
    def CreatePhaseShiftedFields(self, iterationOfSimulation:int):
        """Method changes the phase of the fields. Requires that IdentifyChangingFields
        has run first, to ensure that the items in self.listOfChangingFields are now pointing
        at the correct fields within the totalEMField class.
        Last field generated is one period ahead of the start.
        """
        inverseOfResolution = 1 / self.phaseResolution
        for i in self.listOfPhaseChangingFields:
            i.phaseShift = inverseOfResolution + inverseOfResolution * iterationOfSimulation
    
    def SaveSimulation(self, fileName):
        dictionary = {'Phase':self.simulationPhaseShift, 'FinalSpread':self.simulationFinalSpread}
        dataFrame = pd.DataFrame(dictionary)
        dataFrame.to_pickle("%s.pkl"%(fileName))