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

acceleratingEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e6, 0, 0])
, listOfDimensions=[[-0.5, 0.5], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-3 * const.elementary_charge / const.proton_mass
, name='Accelerating time-varying electric field')

constrainingEField1 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, 1e-1, 0])
, listOfDimensions=[[-1 * scipy.inf, scipy.inf], [-1*scipy.inf, -0.5], [-1 * scipy.inf, scipy.inf]]
, name='Constraining electric field 1')

constrainingEField2 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, -1e-1, 0])
, listOfDimensions=[[-1 * scipy.inf, scipy.inf], [0.5, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, name='Constraining electric field 2')
# note if you don't specify dimensions, it automatically assumes that it is a field
# across all space.
#in addition, if you don't specify angular frequency ie, the field doesn't
# change in time, it assumes a frequency of zero and hence no changing field.
firstBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([1e-4, 0, 0])
, name='First Time Varying Magnetic Field')

secondBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-6, 0])
, name='First Time Varying Magnetic Field')

firstParticleBunch = ParticleBunch(numberOfParticles=10, bunchSpread=1e-26
, bunchMeanEnergy=1.503277592896106e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')
# 1.503277592896106e-10 J of energy to initialise the particles with a mean velocity of 100 m/s

collectionBField = [secondBField]

collectionEField = [acceleratingEField, constrainingEField1, constrainingEField2]

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
        if (firstParticleBunch.listOfParticles[0].position[0] < 0.5 
        and firstParticleBunch.listOfParticles[0].position[0] > -0.5):
            timestep = 1e-8
        # so here we are just using the first proton to give a determination of position for the timestep
        # and it really seems to work.
        simulationState.append(deepcopy(firstParticleBunch.listOfParticles))
        simulationEnergy.append(deepcopy(firstParticleBunch.bunchMeanEnergy))
        simulationSpread.append(deepcopy(firstParticleBunch.bunchSpread))
        simulationTime.append(deepcopy(timeElapsed)) 
        # deepcopy is required to make sure that the "append problem" 
        # is not realiseds
        totalEMField.GiveAcceleration(firstParticleBunch, timeElapsed)
        firstParticleBunch.UpdateBunchMeanEnergy()
        firstParticleBunch.UpdateBunchEnergySpread()
        for i in range(len(firstParticleBunch.listOfParticles)):
            firstParticleBunch.listOfParticles[i].Update(timestep)
        timeElapsed += timestep
    
def SaveSimulation(simulationState, simulationTime, fileName:str):
    dictionary = {'Time':simulationTime, 'Simulation':simulationState
    , 'Energy':simulationEnergy, 'Spread':simulationSpread}
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

def MeanEnergyPlot(pickledFile:str,figureTitle:str, listOfAxisTitles:list):
    fig = plt.figure()
    plt.plot(LoadSim.Time, LoadSim.Energy, label='Energy Plot baby')
    plt.xlabel(listOfAxisTitles[0])
    plt.ylabel(listOfAxisTitles[1])
    plt.title(figureTitle)

    plt.legend()
    plt.show()

def SpreadEnergyPlot(pickledFile:str,figureTitle:str, listOfAxisTitles:list):
    fig = plt.figure()
    plt.plot(LoadSim.Time, LoadSim.Spread, label='Spread Plot baby')
    plt.xlabel(listOfAxisTitles[0])
    plt.ylabel(listOfAxisTitles[1])
    plt.title(figureTitle)

    plt.legend()
    plt.show()

def FirstParticleVelocityPlot(pickledFile:str,figureTitle:str, listOfAxisTitles:list):
    numberOfParticles = len(LoadSim.Simulation[0])
    lengthOfSimulation = len(LoadSim.Time)
    inputData = []
    for i in range(lengthOfSimulation):
        inputData.append(np.linalg.norm(LoadSim.Simulation[i][0].velocity))
               
    fig = plt.figure()
    plt.plot(LoadSim.Time, inputData, label='Velocity Plot baby')
    plt.xlabel(listOfAxisTitles[0])
    plt.ylabel(listOfAxisTitles[1])
    plt.title(figureTitle)
    
    plt.legend()
    plt.show()



    

start = time.time()
ApplyFieldSomeSeconds(2)
end = time.time()
print("Time to simulate is", end - start, "seconds")
fileName = "fuckMe"
SaveSimulation(simulationState, simulationTime, fileName)
# this is currently the only way that I have my loading working.
LoadSim = pd.read_pickle("%s.pkl"%(fileName))
ThreeDPositionPlot(fileName, "Figure Title", ["x position (m)", "y position (m)", "z position (m)"])
MeanEnergyPlot(fileName, "Figure Title", ["Time (s)", "Mean Energy (J)"])
SpreadEnergyPlot(fileName, "Figure Title", ["Time (s)", "Energy Spread Std. (J)"])

FirstParticleVelocityPlot(fileName, "Figure Title", ["Time (s)", "Velocity (m$^{-1}$)"])