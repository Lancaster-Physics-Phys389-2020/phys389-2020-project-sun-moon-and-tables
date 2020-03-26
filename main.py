from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle
from SumEMFields import EMFieldClass
from Plotting import PlottingClass

import scipy.constants as const
import scipy
import numpy as np
import time
import statistics as stats
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy 

acceleratingEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e6, 0, 0])
, listOfDimensions=[[-0.5, 0.5], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-3 * const.elementary_charge / const.proton_mass
, phaseShift=0.0, name='Accelerating time-varying electric field')
# phase shift is in units of 2pi by the way. 

constrainingEField1 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, 1e-1, 0])
, listOfDimensions=[[-1 * scipy.inf, scipy.inf], [-1*scipy.inf, -0.5], [-1 * scipy.inf, scipy.inf]]
, name='Constraining electric field 1')

constrainingEField2 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, -1e-1, 0])
, listOfDimensions=[[-1 * scipy.inf, scipy.inf], [0.5, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, name='Constraining electric field 2')
# note if you don't specify dimensions, it automatically assumes that it is a field
# across all space.
#in addition, if you don't specify angular frequency (or phase shift) ie, the field doesn't
# change in time, it assumes a frequency of zero and hence no changing field.
firstBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([1e-4, 0, 0])
, name='First Time Varying Magnetic Field')

secondBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-6, 0])
, name='First Time Varying Magnetic Field')

firstParticleBunch = ParticleBunch(numberOfParticles=10, bunchSpread=1e-22
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')
# 1.503277592896106e-10 J of energy to initialise the particles with a mean velocity of 10 m/s good spread 5e-26
# 1.5032775928961888e-10 J for 100m/s good spread is 1e-24 (?)
# 1.5032775929044686e-10 J for 1000m/s good spread is 1e-22

collectionBField = [secondBField]

collectionEField = [acceleratingEField]

totalEMField = EMFieldClass(bunchOfParticles=firstParticleBunch
, listOfElectricFields=collectionEField, listOfMagneticFields=collectionBField
, name='First Total EM Field')

simulationState = []
simulationTime = []
simulationEnergy = []
simulationSpread = []
timestep = 1e-3 # if the timestep gets too high, the system seems to jump over the restrictions of special relativity.
# in addition, as the fields become more strong, the timestep needs to be smaller as to ensure special relativity is upheld.
 
def ApplyFieldSomeSeconds(duration):
    timeElapsed = 0.0
    
    while timeElapsed < duration:
        timestep = 1e-3
        meanXPosition = stats.mean([firstParticleBunch.listOfParticles[i].position[0] 
        for i in range(firstParticleBunch.numberOfParticles)])
        if (meanXPosition < 0.5 and meanXPosition > -0.5):
            timestep = 1e-8
        # so here we are just using the first proton to give a determination of position for the timestep
        # and it really seems to work.
        simulationState.append(deepcopy(firstParticleBunch.listOfParticles))
        simulationEnergy.append(deepcopy(firstParticleBunch.bunchMeanEnergy))
        simulationSpread.append(deepcopy(firstParticleBunch.bunchSpread))
        simulationTime.append(deepcopy(timeElapsed)) 
        # deepcopy is required to make sure that the "append problem" 
        # is not realised
        totalEMField.GiveAcceleration(firstParticleBunch, timeElapsed)
        firstParticleBunch.UpdateBunchMeanEnergy(), firstParticleBunch.UpdateBunchEnergySpread()
        for i in range(len(firstParticleBunch.listOfParticles)):
            firstParticleBunch.listOfParticles[i].Update(timestep)
        timeElapsed += timestep
    
def SaveSimulation(fileName:str):
    dictionary = {'Time':simulationTime, 'Simulation':simulationState
    , 'Energy':simulationEnergy, 'Spread':simulationSpread}
    dataFrame = pd.DataFrame(dictionary)
    dataFrame.to_pickle("%s.pkl"%(fileName))

start = time.time()
ApplyFieldSomeSeconds(5e-1)
end = time.time()
print("Time to simulate is", end - start, "seconds")
fileName = "fuckMe"
SaveSimulation(fileName)
plotSimulation = PlottingClass(fileName)
plotSimulation.ThreeDPositionPlot()
plotSimulation.MeanEnergyPlot()
plotSimulation.SpreadEnergyPlot()
