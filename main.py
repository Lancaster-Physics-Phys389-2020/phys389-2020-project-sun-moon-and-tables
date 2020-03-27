from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle
from SumEMFields import EMFieldClass
from Plotting import PlottingClass
from SimulationPhaseChange import SimulationPhaseChangeClass
from SimulationStandard import SimulationStandardClass

# REALLY IMPORTANT TODO: IMPLEMENTING LONGITUDINAL AND TRANSVERSE MASS
# SEE: https://en.wikipedia.org/wiki/Mass_in_special_relativity#Transverse_and_longitudinal_mass
import scipy.constants as const
import scipy
import numpy as np
import time
import statistics as stats
import pandas as pd
from copy import deepcopy 

firstAcceleratingEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e2, 0, 0])
, listOfDimensions=[[-5, 5], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
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

firstParticleBunch = ParticleBunch(numberOfParticles=4, bunchSpread=1e-22
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')
# 1.503277592896106e-10 J of energy to initialise the protons with a mean velocity of 10 m/s good spread 5e-26
# 1.5032775928961888e-10 J for 100m/s good spread is 1e-24 (?)
# 1.5032775929044686e-10 J for 1000m/s good spread is 1e-22

collectionBField = [secondBField]

acceleratingEFields = [firstAcceleratingEField]
confiningEFields = []

totalEMField = EMFieldClass(bunchOfParticles=firstParticleBunch
, listOfElectricFields=acceleratingEFields+confiningEFields, listOfMagneticFields=collectionBField
, name='First Total EM Field')

fileName = "ClassyAttempt2"
start = time.time()

firstSimulation = SimulationStandardClass(totalEMField=totalEMField
, particleBunch=firstParticleBunch, duration=0.25, largeTimestep=1e-3, smallTimestep=1e-6)
secondSimulation = SimulationPhaseChangeClass(listOfPhaseChangingFields=acceleratingEFields
, phaseResolution=50, totalEMField=totalEMField, particleBunch=firstParticleBunch
, duration=0.25, largeTimestep=1e-4, smallTimestep=1e-7)

secondSimulation.RunSimulation()
secondSimulation.SaveSimulation(fileName)
#firstSimulation.RunSimulation()
#firstSimulation.SaveSimulation(fileName)
end = time.time()
print("Time to simulate is", end - start, "seconds")
plotSimulation = PlottingClass(fileName)
plotSimulation.RadialPhaseChangePlot()
