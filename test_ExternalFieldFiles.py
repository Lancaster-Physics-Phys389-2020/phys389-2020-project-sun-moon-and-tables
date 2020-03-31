from GenericField import GenericFieldClass

from AbstractExternalField import AbstractExternalFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from MagneticExternalField import MagneticExternalFieldClass
from Particle import Particle
import numpy as np 
import math
import pytest
import re

test_GenericField = GenericFieldClass(name="test_Generic Field")
test_ElectricExternalField = ElectricExternalFieldClass(electricFieldStrength=np.array([4.0, 5.0, 6.0])
, angularFrequency=10.0, phaseShift=0.1, listOfDimensions=[[-4, 4], [8, 16], [-16, -8]]
, name="test_Electric Field")
test_MagneticExternalField = MagneticExternalFieldClass(magneticFieldStrength=np.array([7.0, 8.0, 9.0])
, angularFrequency=15.0, phaseShift=0.2, listOfDimensions=[[-3, 3], [6, 12], [-12, -6]]
, name="test_Magnetic Field")

test_Particle = Particle(position=np.array([-3.5, 10, -7]),
velocity=np.array([1e6, 1.5e6, 2e6]), acceleration=np.array([2.5e3, 3e3, 3.5e3])
, name='test_Particle', restMass=3.0, charge=7.0)

def test_GenericField__repr__():
    assert re.findall("Field: test_Generic Field", test_GenericField.__repr__()) == ["Field: test_Generic Field"]

def test_ExternalElectricField__repr__():
    assert re.findall("External Electric Field: test_Electric Field", test_ElectricExternalField.__repr__()) == ["External Electric Field: test_Electric Field"]

def test_GenerateElectricField():
    fieldArray = test_ElectricExternalField.GenerateField(timeElapsed=1.0, affectedParticle=test_Particle)
    assert [fieldArray[i] for i in range(3)] == pytest.approx([-1.43622216, -1.7952777 , 0.0], rel=0.05)

def test_ElectricIsParticleInField():
    truthArray = ElectricExternalFieldClass.IsParticleInField(self=test_ElectricExternalField, affectedParticle=test_Particle)
    assert [truthArray[i] for i in range(3)] == [1.0, 1.0, 0.0]

def test_ExternalMagneticField__repr__():
    assert re.findall("External Magnetic Field: test_Magnetic Field", test_MagneticExternalField.__repr__()) == ["External Magnetic Field: test_Magnetic Field"]

def test_MagneticIsParticleInField():
    truthArray = MagneticExternalFieldClass.IsParticleInField(self=test_MagneticExternalField, affectedParticle=test_Particle)
    assert [truthArray[0], truthArray[1], truthArray[2]] == [0.0, 1.0, 1.0]

def test_GenerateMagneticField():
    fieldArray = test_MagneticExternalField.GenerateField(timeElapsed=1.0, affectedParticle=test_Particle)
    assert [fieldArray[i] for i in range(3)] == pytest.approx([0.0, -6.82573571, -7.67895267], rel=0.06)
