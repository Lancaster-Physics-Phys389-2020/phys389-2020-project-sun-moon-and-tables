from AbstractSimulation import AbstractSimulationClass, np, pd, deepcopy, stats
from SumEMFields import EMFieldClass
from ParticleBunchClass import ParticleBunch



class SimulationStandardClass(AbstractSimulationClass):
    """ this class will just do the standard n particle simulation
    that we had already outlined, and prepare the data for
    plotting in the ways that we have outlined too.
    """

    def __init__(self, totalEMField=EMFieldClass, particleBunch=ParticleBunch, duration=1.0
    , largeTimestep=1e-3, smallTimestep=1e-8):
        super().__init__(totalEMField=totalEMField, particleBunch=particleBunch, duration=duration
        , largeTimestep=largeTimestep, smallTimestep=smallTimestep)
        
        self.simulationState = [] # position, velocity, acceleration data
        self.simulationEnergy = [] #mean of enery of particles in simulation
        self.simulationSpread = [] # std deviation of energy of particles in simulation
        self.simulationTime = [] # time of simulation (x axis)

    def RunSimulation(self):
        #runs the standard simulation
        timeElapsed = 0.0
    
        while timeElapsed < self.duration:
            timestep = self.largeTimestep
            meanXPosition = stats.mean([self.particleBunch.listOfParticles[i].position[0] 
            for i in range(self.particleBunch.numberOfParticles)])
            if (meanXPosition < 0.5 and meanXPosition > -0.5):
                timestep = self.smallTimestep
            # so here we are just using the first proton to give a determination of position for the timestep
            # and it really seems to work.
            self.simulationState.append(deepcopy(self.particleBunch.listOfParticles))
            self.simulationEnergy.append(deepcopy(self.particleBunch.bunchMeanEnergy))
            self.simulationSpread.append(deepcopy(self.particleBunch.bunchEnergySpread))
            self.simulationTime.append(deepcopy(timeElapsed)) 
            # deepcopy is required to make sure that the "append problem" 
            # is not realised
            self.totalEMField.GiveAcceleration(self.particleBunch, timeElapsed)
            self.particleBunch.UpdateBunchMeanEnergy(), self.particleBunch.UpdateBunchEnergySpread()
            for i in range(len(self.particleBunch.listOfParticles)):
                self.particleBunch.listOfParticles[i].Update(timestep)
            timeElapsed += timestep
    
    def SaveSimulation(self, fileName):
        # saves the simulation state
        dictionary = {'Time':self.simulationTime, 'Simulation':self.simulationState
        , 'Energy':self.simulationEnergy, 'Spread':self.simulationSpread}
        dataFrame = pd.DataFrame(dictionary)
        dataFrame.to_pickle("%s.pkl"%(fileName))