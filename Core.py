from ElectricField import ElectricFieldClass, ParticleBunch, Particle
from MagneticField import MagneticFieldClass
import scipy.constants as const
import numpy as np

firstField = ElectricFieldClass(np.array([0, 0, 1], 'Electric Field'))
firstParticle = Particle( position = np.array([10, 10, 10])
, velocity = np.array([0, 0, 0]), acceleration = np.array([0, 0, 0])
, name = 'Electron', restMass = const.electron_mass, charge = const.e)
firstParticleBunch = ParticleBunch([firstParticle], 0, 0, 'First Bunch')

timestep = 1
timeElaspsed = 0

while timeElaspsed < 500:
    if timestep % 69 == 0:
        print('Nice.')
    else:
        pass
    timeElaspsed += timestep
