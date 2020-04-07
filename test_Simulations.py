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
import statistics as stats
import pytest
from copy import deepcopy

test_ElectricField = ElectricExternalFieldClass(electricFieldStrength=np.array([1e5, 0, 0])
, listOfDimensions=[[-0.5, 0.5], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-7 * const.elementary_charge / const.proton_mass
, phaseShift=0.0, name='test_Electric Field')

test_ElectricField2 = ElectricExternalFieldClass(electricFieldStrength=np.array([0, 1e2, 0])
, listOfDimensions=[[-100, 100], [-1 * scipy.inf, scipy.inf], [-1 * scipy.inf, scipy.inf]]
, angularFrequency=1e-7 * const.elementary_charge / const.proton_mass
, phaseShift=0.0, name='test_Electric Field')

test_MagneticField = MagneticExternalFieldClass(magneticFieldStrength=np.array([0, 1e-7, 0])
, name='test_Magnetic Field', angularFrequency=0.0, phaseShift=0.0
, listOfDimensions=[[-1*scipy.inf, scipy.inf] for i in range(3)])

test_ParticleBunch = ParticleBunch(numberOfParticles=3, bunchEnergySpread=1e-22, bunchPositionSpread=1e-3
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='test_Particle Bunch')

test_ParticleBunch2 = ParticleBunch(numberOfParticles=3, bunchEnergySpread=1e-22, bunchPositionSpread=1e-3
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='test_Particle Bunch')

test_EMField = EMFieldClass(bunchOfParticles=test_ParticleBunch
, listOfElectricFields=[test_ElectricField], listOfMagneticFields=[test_MagneticField]
, name='test_EM Field')

test_Simulation = SimulationStandardClass(totalEMField=test_EMField
, particleBunch=test_ParticleBunch, duration=1, largeTimestep=1e-3, smallTimestep=1e-6)

test_Simulation2 = SimulationPhaseChangeClass(listOfPhaseChangingFields=[test_ElectricField, test_ElectricField2]
, phaseResolution=12, totalEMField=test_EMField, particleBunch=test_ParticleBunch2
, duration=1, largeTimestep=1e-3, smallTimestep= 1e-6)

def test_StandardRunSimulation():
    # Runs the standard simulation and checks if the mean position of particles at the end of the simulation is correct
    test_Simulation.RunSimulation()
    meanXPosition = stats.mean([test_ParticleBunch.listOfParticles[i].position[0] 
    for i in range(test_ParticleBunch.numberOfParticles)])
    assert meanXPosition == pytest.approx(-121760, rel=0.01)
    
def test_StandardSaveSimulation():
    # Checks if the simulation data is being saved correctly
    assert test_Simulation.simulationTime[1] == 1e-6
    assert test_Simulation.simulationTime[-1] == pytest.approx(1.0, rel=0.01)
    
def test_CreatePhaseShiftedFields():
    # checks that the phase of changing fields are updated correctly
    test_Simulation2.CreatePhaseShiftedFields(iterationOfSimulation=5)
    assert [test_Simulation2.listOfPhaseChangingFields[i].phaseShift for i in range(2)] == [0.5, 0.5]

def test_PhaseChangeRunSimulation():
    # Runs the phase changing simulation and checks if the mean position of particles at the end of the simulation is correct
    test_Simulation2.RunSimulation()
    meanXPosition = stats.mean([test_ParticleBunch.listOfParticles[i].position[0] 
    for i in range(test_ParticleBunch.numberOfParticles)])
    assert meanXPosition == pytest.approx(-121760, rel=0.01)

def test_PhaseChangeSaveSimulation():
    # Checks if the simulation data is being saved correctly and checks the simulation produced the correct results
    finalSpreadList = test_Simulation2.simulationFinalSpread
    copyFinalSpreadList = deepcopy(test_Simulation2.simulationFinalSpread)
    copyFinalSpreadList.remove(min(copyFinalSpreadList))
    minimumSpreadList = [finalSpreadList.index(min(finalSpreadList))
    , copyFinalSpreadList.index(min(copyFinalSpreadList))]
    minimumSpreadList.sort()
    assert test_Simulation2.simulationPhaseShift[-1] == 1.08333
    assert minimumSpreadList == [2,8]