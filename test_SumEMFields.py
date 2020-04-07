from ParticleBunchClass import ParticleBunch
from MagneticExternalField import MagneticExternalFieldClass
from ElectricExternalField import ElectricExternalFieldClass
from SumEMFields import EMFieldClass

import numpy as np 
import math
import scipy.constants as const
import pytest
import re

test_ParticleBunch = ParticleBunch(numberOfParticles=2, bunchPositionSpread=0.0
, bunchEnergySpread=0.0, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass
, chargeOfBunch=1.0, name="test_Bunch")
test_ParticleBunch.listOfParticles[0].position = np.array([1.0, 2.0, 3.0])
test_ParticleBunch.listOfParticles[1].position = np.array([4.0, 5.0, 6.0])
test_ElectricExternalField = ElectricExternalFieldClass(electricFieldStrength=np.array([4.0, 5.0, 6.0])
, angularFrequency=10.0, phaseShift=0.1, listOfDimensions=[[-4, 4], [8, 16], [-16, -8]]
, name="test_Electric Field")
test_MagneticExternalField = MagneticExternalFieldClass(magneticFieldStrength=np.array([7.0, 8.0, 9.0])
, angularFrequency=15.0, phaseShift=0.2, listOfDimensions=[[-3, 3], [6, 12], [-12, -6]]
, name="test_Magnetic Field")
test_EMField = EMFieldClass(bunchOfParticles=test_ParticleBunch, listOfElectricFields=[]
, listOfMagneticFields=[], name="test_EM Field")

def test_EMField__repr__():
    # checks the repr function works
    assert re.findall("EM Field Collection: test_EM Field", test_EMField.__repr__()) == ["EM Field Collection: test_EM Field"]

def test_SumOfEMFields():
    # checks that the total electromagnetic field is added correctly
    assert test_EMField.SumOfEMFields(affectedParticle=test_ParticleBunch.listOfParticles[0]
    , timeElapsed=1.0) == [pytest.approx(np.array([-1.92183905e+08, -1.92183905e+08, -1.92183905e+08]), rel=0.01)
    , pytest.approx(np.array([0.0, 2.13835144e-06, -2.13835144e-06]), rel=0.01)]

def test_GiveAcceleration():
    # checks that the resulting acceleration from the electromagnetic field is correct
    test_EMField.GiveAcceleration(particleBunch=test_ParticleBunch, timeElapsed=1.0)
    assert test_ParticleBunch.listOfParticles[0].acceleration == pytest.approx(
        np.array([-1.1489979e+35, -1.1489979e+35, -1.1489979e+35]), rel=0.01)
