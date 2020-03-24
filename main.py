from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle
from SumEMFields import EMFieldClass

import scipy.constants as const
import scipy
import numpy as np
import time
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy 

firstEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e-3, 0, 0])
, name='First Time Varying Electric Field')

secondEField = ElectricExternalFieldClass(electricFieldStrength=np.array([-1e-4, 0, 0])
, name='Second Time Varying Electric Field')
# note if you don't specify dimensions, it automatically assumes that it is a field
# across all space.
#in addition, if you don't specify angular frequency ie, the field doesn't
# change in time, it assumes a frequency of zero and hence no changing field.
firstBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([1e-4, 0, 0])
, name='First Time Varying Magnetic Field')

secondBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-6, 0])
, name='First Time Varying Magnetic Field')

"""
firstParticle = Particle(position=np.array([0, 0, 1e-10])
, velocity=np.array([1, 10, 0]), acceleration=np.array([0, 0, 0])
, name='Proton1', restMass=const.proton_mass, charge=1 * const.elementary_charge)

secondParticle = Particle(position=np.array([0, 0, 0])
, velocity=np.array([1, 10, 0]), acceleration=np.array([0, 0, 0])
, name='Proton2', restMass=const.proton_mass, charge=1 * const.elementary_charge)
"""

firstParticleBunch = ParticleBunch(numberOfParticles=5, bunchSpread=1e-26
, bunchMeanEnergy=1.503277592896106e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')
# 1.503277592896106e-10 J of energy to initialise the particles with a mean velocity of 100 m/s

collectionBField = [secondBField]

collectionEField = []

totalEMField = EMFieldClass(bunchOfParticles=firstParticleBunch
, listOfElectricFields=collectionEField, listOfMagneticFields=collectionBField
, name='First Total EM Field')

simulationState = []
simulationTime = []
timestep = 1e-4 # if the timestep gets too high, the system seems to jump over the restrictions of special relativity.
# in addition, as the fields become more strong, the timestep needs to be smaller as to ensure special relativity is upheld.

def ApplyFieldSomeSeconds(duration):
    timeElapsed = 0.0
    
    while timeElapsed < duration:
        # perhaps consider what Ryan suggested with a variable timestep depending on
        # whether the particle is being acceleraed by the electric field
        simulationState.append(deepcopy(firstParticleBunch.listOfParticles)) 
        simulationTime.append(deepcopy(timeElapsed)) 
        # deepcopy is required to make sure that the "append problem" 
        # is not realised
        totalEMField.GiveAcceleration(firstParticleBunch, timeElapsed)
        for i in range(len(firstParticleBunch.listOfParticles)):
            firstParticleBunch.listOfParticles[i].Update(timestep)
        timeElapsed += timestep
    

def SaveSimulation(simulationState, simulationTime, fileName:str):
    dictionary = {'Time':simulationTime, 'Simulation':simulationState}
    dataFrame = pd.DataFrame(dictionary)
    dataFrame.to_pickle("%s.pkl"%(fileName))

def LoadSimulation(pickledFile:str): 
    # this seems to be an inefficient method of loading the simulation
    # method suggested by Tom is futher down, where fileName is defined.
    return pd.read_pickle("%s.pkl"%(pickledFile))

def ThreeDPositionPlot(pickledFile:str,figureTitle:str, listOfAxisTitles:list):
    numberOfParticles = len(LoadSim.Simulation[0])
    lengthOfSimulation = len(LoadSim.Time)
    inputData = [[[], [], []] for i in range(numberOfParticles)]
    # creates a list per particle.
    for i in range(lengthOfSimulation):
        for j in range(numberOfParticles):
            for k in range(3):
                inputData[j][k].append(LoadSim.Simulation[i][j].position[k])
                # so this is the one line that does position. could swap this out
                # for different simulation properties.

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for j in range(numberOfParticles):
        ax.plot(inputData[j][0], inputData[j][1], inputData[j][2]
        , label='%s'%(LoadSim.Simulation[0][j].name))
    ax.set_xlabel(listOfAxisTitles[0])
    ax.set_ylabel(listOfAxisTitles[1])
    ax.set_zlabel(listOfAxisTitles[2])

    ax.legend()
    plt.show()

start = time.time()
ApplyFieldSomeSeconds(1) # WARNING, A LONG SIMULATION SEEMS TO STOP THE PLOTTING FROM WORKING!
end = time.time()
print("Time to simulate is", end - start, "seconds")
fileName = "fuckMe"
SaveSimulation(simulationState, simulationTime, fileName)
# this is currently the only way that I have my loading working.
LoadSim = pd.read_pickle("%s.pkl"%(fileName))
ThreeDPositionPlot(fileName, "Figure Title", ["x position (m)", "y position (m)", "z position (m)"])