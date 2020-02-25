from ElectricField import ElectricFieldClass, ParticleBunch, Particle
from MagneticField import MagneticFieldClass
import scipy.constants as const
import numpy as np

firstField = ElectricFieldClass(electricFieldStrength=np.array([0, 0, 0.05])
, name='First Electric Field')
firstParticle = Particle(position=np.array([10, 10, 10])
, velocity=np.array([0, 0, 0]), acceleration=np.array([0, 0, 0])
, name='Electron', restMass=const.electron_mass, charge=-1 * const.elementary_charge)
secondParticle = Particle(position=np.array([10, 10, -2000])
, velocity=np.array([0, 0, 0]), acceleration=np.array([0, 0, 0])
, name='Proton', restMass=const.proton_mass, charge=const.elementary_charge)
firstParticleBunch = ParticleBunch([firstParticle, secondParticle], 0, 0, 'First Bunch')

timestep = 1e-3

def Returner():
    return firstField, firstParticleBunch

def ApplyFieldSomeSeconds(duration):
    timeElaspsed = 0
    
    while timeElaspsed < duration:
        for i in range(len(firstParticleBunch.listOfParticles)):
            print(firstParticleBunch.listOfParticles[i].name
            , 'Velocity:', firstParticleBunch.listOfParticles[i].velocity
            , 'Acceleration:', firstParticleBunch.listOfParticles[i].acceleration
            , 'Lorentz Factor:'
            , firstParticleBunch.listOfParticles[i].LorentzFactor())
        firstField.GiveAcceleration(firstParticleBunch)
        for i in range(len(firstParticleBunch.listOfParticles)):
            firstParticleBunch.listOfParticles[i].Update(timestep)
        timeElaspsed += timestep

ApplyFieldSomeSeconds(1)


