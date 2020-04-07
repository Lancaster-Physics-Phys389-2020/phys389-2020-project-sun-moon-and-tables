from Particle import Particle
from AbstractPointField import AbstractPointFieldClass
from PointElectricField import PointElectricFieldClass
from PointMagneticField import PointMagneticFieldClass
from SumEMFields import EMFieldClass

import numpy as np 
import math
import scipy
import pytest
import re

test_Particle = Particle(position=np.array([10, 100, 1000]),
velocity=np.array([1e6, 1.5e6, 2e6]), acceleration=np.array([2.5e3, 3e3, 3.5e3])
, name='test_Particle', restMass=3.0, charge=7.0)

test_Particle2 = Particle(position=np.array([4, 3, 2]),
velocity=np.array([2.5e6, 3e6, 3.5e6]), acceleration=np.array([1.0, 9.0, 2.0])
, name='test_Particle2', restMass=3.0, charge=14.0)

test_PointElectricField = PointElectricFieldClass(sourceParticle=test_Particle, name="test_Particle Electric Field")
test_PointMagneticField = PointMagneticFieldClass(sourceParticle=test_Particle, name="test_Particle Magnetic Field")

def test_PointElectricField__repr__():
    # test that the repr function works
    assert re.findall(
        "Electric Point Field: test_Particle Electric Field", test_PointElectricField.__repr__()) == ["Electric Point Field: test_Particle Electric Field"]

def test_GenerateElectricField():
    # test that the electric field is calculated correctly
    assert test_PointElectricField.GenerateField(test_Particle2) == pytest.approx(
        np.array([-374.41274741, -6053.00608319, -62277.32031987]), rel=0.06)

def test_PointMagneticField__repr__():
    # test that the repr function works
    assert re.findall(
        "Magnetic Point Field: test_Particle Magnetic Field", test_PointMagneticField.__repr__()) == ["Magnetic Point Field: test_Particle Magnetic Field"]

def test_GenerateMagneticField():
    # test that the magnetic field is calculated correctly
    assert test_PointMagneticField.GenerateField(test_Particle2) == pytest.approx(
        np.array([-9.04695408e-07,  6.84596832e-07, -6.10999201e-08]), rel=0.06)
