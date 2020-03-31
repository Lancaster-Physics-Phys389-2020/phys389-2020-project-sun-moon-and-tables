from ParticleBunchClass import ParticleBunch, np, math, const, Particle
import re
import pytest

test_ParticleBunch = ParticleBunch(numberOfParticles=1000, bunchPositionSpread=1.0
, bunchEnergySpread=1e-22, bunchMeanEnergy=1.5032775929044686e-10, restMassOfBunch=const.proton_mass
, chargeOfBunch=1.0, name="test_Bunch")

def test_ParticleBunch__repr__():
    # checks the repr function works
    assert re.findall("Name: test_Bunch 1", test_ParticleBunch.listOfParticles[0].__repr__()) == ["Name: test_Bunch 1"]

def test_CreateListOfParticles():
    # check that the correct number of particles are initialised
    assert len(test_ParticleBunch.listOfParticles) == 1000
    # check that the particles that are made are with the correct spread in position
    assert np.std([test_ParticleBunch.listOfParticles[i].position for i in range(test_ParticleBunch.numberOfParticles)]) == pytest.approx(1.0, abs=0.07)
    # check that the particles have the correct mean position
    assert np.mean([test_ParticleBunch.listOfParticles[i].position for i in range(test_ParticleBunch.numberOfParticles)]) == pytest.approx(0.0, abs=0.07)

def test_CreateVelocitySpread():
    # check that the particles have the correct velocity spread
    assert np.std(test_ParticleBunch.CreateVelocitySpread()) == pytest.approx(60, rel=0.07)
    # check that the particles have the correct mean velocity
    assert np.mean(test_ParticleBunch.CreateVelocitySpread()) == pytest.approx(1000, rel=0.05)

def test_UpdateBunchMeanEnergy():
    test_ParticleBunch.UpdateBunchMeanEnergy()
    # check that the mean energy of the randomly generated bunch is calculated correctly
    assert test_ParticleBunch.bunchMeanEnergy == pytest.approx(1.5032775929044686e-10, rel=0.06)

def test_UpdateBunchEnergySpread():
    test_ParticleBunch.UpdateBunchEnergySpread()
    # check that the standard deviation of the randomly generated bunch is calculated correctly
    assert test_ParticleBunch.bunchEnergySpread == pytest.approx(1e-22, rel=0.08)

def test_FindBunchMeanVelocity():
    # checks that the method for finding the mean velocity of particles in the bunch is correct
    assert test_ParticleBunch.FindBunchMeanVelocity()[0] == pytest.approx(1000, rel=0.05)
