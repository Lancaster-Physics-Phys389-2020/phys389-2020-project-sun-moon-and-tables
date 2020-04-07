from GenericField import GenericFieldClass

from AbstractExternalField import AbstractExternalFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from MagneticSynchrotronField import MagneticSynchrotronFieldClass
from Particle import Particle
from ParticleBunchClass import ParticleBunch
import numpy as np 
import math
import pytest
import scipy.constants as const
import re

test_GenericField = GenericFieldClass(name="test_Generic Field")
test_ElectricExternalField = ElectricExternalFieldClass(electricFieldStrength=np.array([4.0, 5.0, 6.0])
, angularFrequency=10.0, phaseShift=0.1, listOfDimensions=[[-4, 4], [8, 16], [-16, -8]]
, name="test_Electric Field")
test_MagneticExternalField = MagneticExternalFieldClass(magneticFieldStrength=np.array([7.0, 8.0, 9.0])
, angularFrequency=15.0, phaseShift=0.2, listOfDimensions=[[-5, 5], [6, 12], [-12, -6]]
, name="test_Magnetic Field")
test_Particle = Particle(position=np.array([-3.5, 10, -7]),
velocity=np.array([1e6, 1.5e6, 2e6]), acceleration=np.array([2.5e3, 3e3, 3.5e3])
, name='test_Particle', restMass=3.0, charge=7.0)
test_ParticleBunch = ParticleBunch(numberOfParticles=3, bunchEnergySpread=1e-22, bunchPositionSpread=1e-3
, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass, chargeOfBunch=const.elementary_charge
, name='test_Particle Bunch')
test_MagneticSynchrotronField = MagneticSynchrotronFieldClass(magneticFieldStrength=np.array([7.0, 8.0, 9.0])
, angularFrequency=15.0, phaseShift=0.2, listOfDimensions=[[-5, 5], [-6, 12], [-12, 6]]
, name="test_Magnetic Synchrotron Field", particleBunch=test_ParticleBunch)

def test_GenericField__repr__():
    # checks the repr function works
    assert re.findall(
        "Field: test_Generic Field", test_GenericField.__repr__()) == ["Field: test_Generic Field"]

def test_ExternalElectricField__repr__():
    # checks the repr function works
    assert re.findall(
        "External Electric Field: test_Electric Field", test_ElectricExternalField.__repr__()) == ["External Electric Field: test_Electric Field"]

def test_GenerateElectricField():
    # test that an external electric field with specified dimensions works
    fieldArray = test_ElectricExternalField.GenerateField(timeElapsed=1.0, affectedParticle=test_Particle)
    assert [fieldArray[i] for i in range(3)] == [0.0, 0.0 , 0.0]

def test_ElectricIsParticleInField():
    # test that the particle is correctly detected in the electric field
    truthValue = ElectricExternalFieldClass.IsParticleInField(self=test_ElectricExternalField, affectedParticle=test_Particle)
    assert truthValue == 0.0

def test_ExternalMagneticField__repr__():
    # checks the repr function works
    assert re.findall(
        "External Magnetic Field: test_Magnetic Field", test_MagneticExternalField.__repr__()) == ["External Magnetic Field: test_Magnetic Field"]

def test_MagneticIsParticleInField():
    # test that the particle is correctly detected in the electric field
    truthValue = MagneticExternalFieldClass.IsParticleInField(self=test_MagneticExternalField, affectedParticle=test_Particle)
    assert truthValue == 1.0

def test_GenerateMagneticField():
    # test that an external amgnetic field with specified dimensions works
    fieldArray = test_MagneticExternalField.GenerateField(timeElapsed=1.0, affectedParticle=test_Particle)
    assert [fieldArray[i] for i in range(3)] == pytest.approx([-5.97251874, -6.82573571, -7.67895267], rel=0.06)

def test_MagneticSynchrotronField__repr__():
    assert re.findall(
        "Magnetic Synchrotron Field: test_Magnetic Synchrotron Field", test_MagneticSynchrotronField.__repr__()) == ["Magnetic Synchrotron Field: test_Magnetic Synchrotron Field"]

def test_SynchrotronConstantRadius():
    assert test_MagneticSynchrotronField.ConstantRadius() == pytest.approx(1.0, rel=0.01)

def test_GenerateSynchrotronMagneticField():
    fieldArray = test_MagneticSynchrotronField.GenerateField(timeElapsed=1.0, affectedParticle=test_ParticleBunch.listOfParticles[0])
    assert [fieldArray[i] for i in range(3)] == pytest.approx([-5.97251874, -6.82573571, -7.67895267], rel=0.06)

