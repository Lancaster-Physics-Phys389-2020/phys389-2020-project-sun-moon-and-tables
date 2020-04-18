from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from ParticleBunchClass import ParticleBunch, Particle
from SumEMFields import EMFieldClass
from Plotting import PlottingClass
from SimulationPhaseChange import SimulationPhaseChangeClass
from SimulationStandard import SimulationStandardClass
from SimulationConservationLaws import SimulationConservationLawsClass

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

test_ParticleBunch3 = ParticleBunch(numberOfParticles=2, bunchEnergySpread=0.0
, bunchMeanEnergy=1.5032775928961087e-10, restMassOfBunch=const.proton_mass
, chargeOfBunch=const.elementary_charge, bunchPositionMean=0.5e-2, bunchPositionSpread=1e-4
, name="test_Particle Bunch")

test_ParticleBunch3.listOfParticles[1].charge = -1 * test_ParticleBunch3.chargeOfBunch
test_ParticleBunch3.listOfParticles[1].velocity = -1 * test_ParticleBunch3.listOfParticles[0].velocity
test_ParticleBunch3.listOfParticles[0].position = np.array([0.00501547, 0.00493024, 0.00498064])
test_ParticleBunch3.listOfParticles[1].position = np.array([0.0048881,  0.00503995, 0.00492297])

test_EMField = EMFieldClass(bunchOfParticles=test_ParticleBunch
, listOfElectricFields=[test_ElectricField], listOfMagneticFields=[test_MagneticField]
, name='test_EM Field')

test_ClearEMField = EMFieldClass(bunchOfParticles=test_ParticleBunch3, listOfElectricFields=[]
, listOfMagneticFields=[], name="test_EM Field")

test_Simulation = SimulationStandardClass(totalEMField=test_EMField
, particleBunch=test_ParticleBunch, duration=1, largeTimestep=1e-3, smallTimestep=1e-6)

test_Simulation2 = SimulationPhaseChangeClass(listOfPhaseChangingFields=[test_ElectricField, test_ElectricField2]
, phaseResolution=12, totalEMField=test_EMField, particleBunch=test_ParticleBunch2
, duration=1, largeTimestep=1e-3, smallTimestep= 1e-6)

test_Simulation3 = SimulationConservationLawsClass(totalEMField=test_ClearEMField, particleBunch=test_ParticleBunch3
, duration=1e-5, largeTimestep=1e-7, spaceResolution=1)


def test_StandardRunSimulation():
    # Runs the standard simulation and checks if the mean position of particles at the end of the simulation is correct
    test_Simulation.RunSimulation()
    meanXPosition = stats.mean([test_ParticleBunch.listOfParticles[i].position[0] 
    for i in range(test_ParticleBunch.numberOfParticles)])
    assert meanXPosition == pytest.approx(-174640, rel=0.01)
    
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
    assert meanXPosition == pytest.approx(-174640, rel=0.01)

def test_PhaseChangeSaveSimulation():
    # Checks if the simulation data is being saved correctly and checks the simulation produced the correct results
    finalSpreadList = test_Simulation2.simulationFinalSpread
    copyOfFinalSpreadList = deepcopy(test_Simulation2.simulationFinalSpread)
    copyOfFinalSpreadList.remove(min(copyOfFinalSpreadList))
    minimumSpreadList = [finalSpreadList.index(min(finalSpreadList)), copyOfFinalSpreadList.index(min(copyOfFinalSpreadList))]
    minimumSpreadList.sort()
    assert test_Simulation2.simulationPhaseShift[-1] == 1.08333
    assert minimumSpreadList == [2,8]

def test_CreateListOfPositions():
    # checks that the list of positions is updated correctly
    assert test_Simulation3.listOfPositions[1].tolist() == [0.0, 0.0, 0.001]

def test_CreateDictionary():
    # checks that the dictionary of energies are created correctly
    assert test_Simulation3.dictionaryOfEnergyDensity[(0.0, 0.0, 0.001)] == None

def test_EnergyDensity():
    # checks that the energy density is calculated correctly
    test_Simulation3.dummyParticle.position == np.array([0.0, 0.0, 0.0])
    assert test_Simulation3.EnergyDensity(timeElapsed=0.0) == pytest.approx(8.4e-25, rel=0.01)

def test_DictionaryOfEnergyDensity():
    # checks that the dictionary of energy density is updated correctly
    test_Simulation3.DictionaryOfEnergyDensity(timeElapsed=0.0)
    assert test_Simulation3.dictionaryOfEnergyDensity[(0.0, 0.0, 0.0)] == pytest.approx(8.4e-25, rel=0.01)

def test_IntegrateEnergyDensity():
    # checks that total energy is integrated correctly from energy density
    assert test_Simulation3.IntegrateEnergyDensity(timeElapsed=0.0) == pytest.approx(1e-32, rel=0.01)

def test_ConservationLawRunSimulation():
    # checks that the simulation runs correctly and the final position of both particles are accurate
    test_Simulation3.RunSimulation()
    assert test_Simulation3.particleBunch.listOfParticles[0].position == pytest.approx(
        np.array([0.00510592, 0.00498373, 0.00495252]), rel=0.01)
    assert test_Simulation3.particleBunch.listOfParticles[1].position == pytest.approx(
        np.array([0.00479765, 0.00498646, 0.00495109]), rel=0.01)

def test_ConservationLawSaveSimulation():
    # checks that the data from the simulation is calculated and saved correctly
    assert test_Simulation3.simulationMomentum[0] == 0.0
    assert test_Simulation3.simulationAngularMomentum[0] == pytest.approx(4.1e-30, rel=0.01)
    assert test_Simulation3.simulationTime[-1] == pytest.approx(1e-5, rel=0.01)
    assert test_Simulation3.simulationEnergyParticles[0] == pytest.approx(6.7e-25, rel=0.01)
    assert test_Simulation3.simulationEnergyFields[0] == pytest.approx(1e-32, rel=0.01)