from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from MagneticSynchrotronField import MagneticSynchrotronFieldClass
from ParticleBunchClass import ParticleBunch
from SumEMFields import EMFieldClass
from Plotting import PlottingClass
from SimulationPhaseChange import SimulationPhaseChangeClass
from SimulationStandard import SimulationStandardClass
from SimulationConservationLaws import SimulationConservationLawsClass

import scipy.constants as const
import scipy
import numpy as np
import math

cyclotronParticleBunch = ParticleBunch(numberOfParticles=4, bunchEnergySpread=1e-22, bunchPositionSpread=1e-3
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')
# 1.503277592896106e-10 J of energy to initialise the protons with a mean velocity of 10 m/s good spread 5e-26
# 1.5032775928961888e-10 J for 100m/s good spread is 1e-24
# 1.5032775929044686e-10 J for 1000m/s good spread is 1e-22

cyclotronEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e4, 0, 0])
, listOfDimensions=[[-1, 1], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-6 * const.elementary_charge / const.proton_mass
, phaseShift=0.0, name='cyclotronEField')
# phase shift is measured as a fraction of a period

cyclotronBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-6, 0])
, name='cyclotronBField')

cyclotronEMField = EMFieldClass(bunchOfParticles=cyclotronParticleBunch
, listOfElectricFields=[cyclotronEField], listOfMagneticFields=[cyclotronBField]
, name='cyclotronEMField')

cyclotronSimulation = SimulationStandardClass(totalEMField=cyclotronEMField
, particleBunch=cyclotronParticleBunch, duration=3, largeTimestep=5e-4, smallTimestep=1e-6)

# Run conditions for the example Cyclotron Simulation
cyclotronSimulation.RunSimulation()
cyclotronSimulation.SaveSimulation("cyclotron")
cyclotronPlot = PlottingClass("cyclotron")
cyclotronPlot.ThreeDPositionPlot()
cyclotronPlot.MeanParticleVelocityPlot()
cyclotronPlot.MeanEnergyPlot()

synchrotronParticleBunch = ParticleBunch(numberOfParticles=1, bunchEnergySpread=1e-22, bunchPositionSpread=1e-6
, bunchMeanEnergy=3.5356655116389166e-08, restMassOfBunch=92*const.proton_mass+143*const.neutron_mass
, chargeOfBunch=92* const.elementary_charge
, name='Uranium')
# 3.5356655116389166e-08 J of energy to initialise uranium atoms with 1000m/s

synchrotronBField = MagneticSynchrotronFieldClass(magneticFieldStrength=np.array([0, 6e-8, 0])
, name='synchotronBField', particleBunch=synchrotronParticleBunch)

synchrotronRadius = (np.linalg.norm(synchrotronParticleBunch.FindBunchMeanMomentum())
/ (np.linalg.norm(synchrotronBField.fieldStrength) * synchrotronParticleBunch.chargeOfBunch))

synchrotronEField1 = ElectricExternalFieldClass(electricFieldStrength=np.array([3e4, 0, 0])
, listOfDimensions=[[-1, 1], [-1 * scipy.inf, scipy.inf], [-1, 1]], name='synchrotronEField1')

synchrotronEField2 = ElectricExternalFieldClass(electricFieldStrength=np.array([-3e4, 0, 0])
, listOfDimensions=[[-1, 1], [-1 * scipy.inf, scipy.inf], [2 * synchrotronRadius - 1, 2 * synchrotronRadius + 1]]
, name='synchrotronEField2')

synchrotronEMField = EMFieldClass(bunchOfParticles=synchrotronParticleBunch
, listOfElectricFields=[synchrotronEField1, synchrotronEField2], listOfMagneticFields=[synchrotronBField]
, name='synchrotronEMField')

synchrotronSimulation = SimulationStandardClass(totalEMField=synchrotronEMField
, particleBunch=synchrotronParticleBunch, duration=0.0145, largeTimestep=1e-7, smallTimestep=5e-8)

# Run conditions for the example Synchrotron Simulation
synchrotronSimulation.RunSimulation()
synchrotronSimulation.SaveSimulation("synchrotron")
synchrotronPlot = PlottingClass("synchrotron")
synchrotronPlot.ThreeDPositionPlot()
synchrotronPlot.MeanParticleVelocityPlot()
synchrotronPlot.MeanEnergyPlot()

phaseChangeParticleBunch = ParticleBunch(numberOfParticles=3, bunchEnergySpread=1e-22, bunchPositionSpread=1e-2
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='Proton')

phaseChangeEField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e5, 0, 0])
, listOfDimensions=[[-1, 1], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-7 * const.elementary_charge / const.proton_mass
, phaseShift=0.0, name='Phase change time-varying electric field')

phaseChangeBField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-7, 0])
, name='Phase change constant magnetic field')

phaseChangeEMField = EMFieldClass(bunchOfParticles=phaseChangeParticleBunch
, listOfElectricFields=[phaseChangeEField], listOfMagneticFields=[phaseChangeBField]
, name='Phase change EM field')

phaseChangeSimulation = SimulationPhaseChangeClass(listOfPhaseChangingFields=[phaseChangeEField]
, phaseResolution=48, totalEMField=phaseChangeEMField, particleBunch=phaseChangeParticleBunch
, duration=0.5, largeTimestep=5e-4, smallTimestep=1e-6)

# Run conditions for the example Change of Phase Simulation

fileNamePhaseChange = "phase change simulation"
phaseChangeSimulation.RunSimulation()
phaseChangeSimulation.SaveSimulation(fileNamePhaseChange)
plotSimulationPhaseChange = PlottingClass(fileNamePhaseChange)
plotSimulationPhaseChange.RadialPhaseChangePlot()
plotSimulationPhaseChange.PhaseChangePlot("log")

conservationParticleBunch = ParticleBunch(numberOfParticles=2, bunchEnergySpread=0.0
, bunchMeanEnergy=1.5032775928961087e-10, restMassOfBunch=const.proton_mass
, chargeOfBunch=const.elementary_charge, bunchPositionMean=0.5e-2, bunchPositionSpread=1e-4
, name="Proton")
# proton at 40m/s 1.5032775928961187e-10 J
# proton at 20m/s 1.5032775928961087e-10 J 

conservationEMField = EMFieldClass(bunchOfParticles=conservationParticleBunch, listOfElectricFields=[]
, listOfMagneticFields=[], name="Conservation Law EM Field")

conservationLawSimulation = SimulationConservationLawsClass(totalEMField=conservationEMField
, particleBunch=conservationParticleBunch, duration=10e-5, largeTimestep=1e-7, spaceResolution=4)

# optional changes to ensure a stable simulation
for i in range(math.floor(conservationParticleBunch.numberOfParticles / 2)):
# this alternates the charge and the starting velocity of initial particles
    conservationParticleBunch.listOfParticles[2*i+1].charge = -1 * conservationParticleBunch.chargeOfBunch
    conservationParticleBunch.listOfParticles[2*i+1].name = "Anti-proton %s"%(math.ceil((2*i+1)/2))
    conservationParticleBunch.listOfParticles[2*i+1].velocity = -1 * conservationParticleBunch.listOfParticles[0].velocity
# for a proton anti-proton pair, these initial positions are good for creating a oscillating system
conservationParticleBunch.listOfParticles[0].position = np.array([0.00501547, 0.00493024, 0.00498064])
conservationParticleBunch.listOfParticles[1].position = np.array([0.0048881,  0.00503995, 0.00492297])

# Run conditions for the Simulation to test conservation laws

fileNameConservationLaw = "conservation law simulation"
conservationLawSimulation.RunSimulation()
conservationLawSimulation.SaveSimulation(fileNameConservationLaw)
plotConservationLaw = PlottingClass(fileNameConservationLaw)
plotConservationLaw.ThreeDPositionPlot()
plotConservationLaw.ConservationOfEnergyFieldsPlot()
plotConservationLaw.ConservationOfEnergyParticlesPlot()
plotConservationLaw.ConservationOfAngMomentumPlot()
plotConservationLaw.ConservationOfMomentumPlot()