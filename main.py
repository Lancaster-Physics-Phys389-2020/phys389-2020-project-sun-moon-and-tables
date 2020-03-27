from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle
from SumEMFields import EMFieldClass
from Plotting import PlottingClass
from SimulationPhaseChange import SimulationPhaseChangeClass
from SimulationStandard import SimulationStandardClass

import scipy.constants as const
import scipy
import numpy as np
import time
import statistics as stats
import pandas as pd
from copy import deepcopy 

firstAcceleratingEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e6, 0, 0])
, listOfDimensions=[[-0.5, 0.5], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-5 * const.elementary_charge / const.proton_mass
, phaseShift=0.0, name='Accelerating time-varying electric field')
# phase shift is in units of 2pi by the way. 

constrainingEField1 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, 1e1, 0])
, listOfDimensions=[[-1 * scipy.inf, scipy.inf], [-1*scipy.inf, -0.5], [-1 * scipy.inf, scipy.inf]]
, name='Constraining electric field 1')

constrainingEField2 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, -1e1, 0])
, listOfDimensions=[[-1 * scipy.inf, scipy.inf], [0.5, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, name='Constraining electric field 2')
# note if you don't specify dimensions, it automatically assumes that it is a field
# across all space.
#in addition, if you don't specify angular frequency (or phase shift) ie, the field doesn't
# change in time, it assumes a frequency of zero and hence no changing field.
firstBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-5, 0])
, name='First Time Varying Magnetic Field')

firstParticleBunch = ParticleBunch(numberOfParticles=2, bunchEnergySpread=1e-22, bunchPositionSpread=1e-3
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')
# 1.503277592896106e-10 J of energy to initialise the protons with a mean velocity of 10 m/s good spread 5e-26
# 1.5032775928961888e-10 J for 100m/s good spread is 1e-24 (?)
# 1.5032775929044686e-10 J for 1000m/s good spread is 1e-22

secondParticleBunch = ParticleBunch(numberOfParticles=2, bunchEnergySpread=1e-20, bunchPositionSpread=1e-3
, bunchMeanEnergy=3.5356655116389166e-08, restMassOfBunch=92*const.proton_mass+143*const.neutron_mass
, chargeOfBunch=92*const.elementary_charge, name='Uranium')
# 3.5356655116389166e-08 J of energy to initialise uranium atoms with 1000m/s

collectionBField = [firstBField]

acceleratingEFields = [firstAcceleratingEField]
confiningEFields = []

totalEMField = EMFieldClass(bunchOfParticles=firstParticleBunch
, listOfElectricFields=acceleratingEFields+confiningEFields, listOfMagneticFields=collectionBField
, name='First Total EM Field')

firstSimulation = SimulationStandardClass(totalEMField=totalEMField
, particleBunch=secondParticleBunch, duration=0.25, largeTimestep=1e-4, smallTimestep=1e-6)

secondSimulation = SimulationPhaseChangeClass(listOfPhaseChangingFields=acceleratingEFields
, phaseResolution=20, totalEMField=totalEMField, particleBunch=secondParticleBunch
, duration=0.5, largeTimestep=1e-4, smallTimestep=1e-6)

fileName1 = "file name of simulation 1"
fileName2 = "file name of simulation 2"
start = time.time()

firstSimulation.RunSimulation()
firstSimulation.SaveSimulation(fileName1)
end = time.time()
print("Time to simulate is", end - start, "seconds")
plotSimulation1 = PlottingClass(fileName1)
plotSimulation1.ThreeDPositionPlot()
plotSimulation1.FirstParticleVelocityPlot()

#secondSimulation.RunSimulation()
#secondSimulation.SaveSimulation(fileName2)
#plotSimulation2 = PlottingClass(fileName2)