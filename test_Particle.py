from Particle import Particle, np, math, const, PointElectricFieldClass, PointMagneticFieldClass
import pytest
import re


test_Particle = Particle(position=np.array([10, 100, 1000]),
velocity=np.array([1e6, 1.5e6, 2e6]), acceleration=np.array([2.5e3, 3e3, 3.5e3])
, name='test_Particle', restMass=3.0, charge=7.0)

test_Particle2 = Particle(position=np.array([10, 100, 1000]),
velocity=np.array([1e6, 1.5e6, 2e6]), acceleration=np.array([2.5e3, 3e3, 3.5e3])
, name='test_Particle2', restMass=3.0, charge=7.0)

def test_Particle__repr__():
    # checks the repr function works
    assert re.findall("Name: test_Particle", test_Particle.__repr__()) == ["Name: test_Particle"]

def test_RestEnergy():
    # checks that rest energy is calculated correctly
    assert test_Particle.RestEnergy() == pytest.approx(2.6962655362104528e+17)

def test_BetaVector():
    # checks that Beta is calculated correctly
    assert test_Particle.BetaVector() == pytest.approx(np.array([0.00333564, 0.00500346, 0.00667128]))

def test_LorentzFactor():
    # checks Lorentz factor is calculated correctly
    assert test_Particle.LorentzFactor() == pytest.approx(1.0008519068013697)

def test_RelativisticMass():
    assert test_Particle.RelativisticMass() == pytest.approx(3.002555720404109)
    # worth mentioning that relativistic mass is not acting as a vector, because
    # this caused problems with the magnetic field, the mass vector would not be
    # correct for updates of acceleration and resulted in strange energy behaviour.

def test_Momentum():
    # checks momentum is calculated correctly
    assert test_Particle.Momentum() == pytest.approx(np.array([3002555.72040411, 4503833.58060616, 6005111.44080822]))

def test_TotalEnergy():
    # checks total energy is calculated correctly
    assert test_Particle.TotalEnergy() == pytest.approx(2.6963744693785754e+17)

def test_KineticEnergy():
    # checks kinetic energy is calculated correctly
    assert test_Particle.KineticEnergy() == pytest.approx(10893316812256.0)

def test_Update():
    test_Particle.Update(1.0)
    # updates a particle with the euler cromer method and checks the position and acceleration is updated correctly
    assert test_Particle.velocity == pytest.approx(np.array([1002500., 1503000., 2003500.]))
    assert test_Particle.position == pytest.approx(np.array([1002510., 1503100., 2004500.]))

def test_Update2():
    test_Particle2.Update2(1.0)
    # updates a particle with the euler forward method and checks the position and acceleration is updated correctly
    assert test_Particle2.position == pytest.approx(np.array([1000010., 1500100., 2001000.]))
    assert test_Particle2.velocity == pytest.approx(np.array([1002500., 1503000., 2003500.]))

def test_GenerateElectricField():
    # check that an electric field can be created by a particle and is the correct vector at a distance
    assert test_Particle.electricField.GenerateField(test_Particle2) == pytest.approx(np.array([-8.55023151e-20, -1.02602778e-19, -1.19703241e-19]))

def test_GenerateMagneticField():
    # check that a magnetic field can be created by a particle and is the correct vector at a distance
    assert test_Particle.magneticField.GenerateField(test_Particle2) == pytest.approx(np.array([3.64049352e-09, -7.28098705e-09,  3.64049352e-09]))