import numpy as np
import math
import scipy.constants as const

velocity = np.array([0, 0, 1.7e+07])

def BetaVector():
        return velocity / const.speed_of_light

def LorentzFactor():
    return 1 / (1 - math.sqrt(1 - np.linalg.norm(BetaVector())
        * np.linalg.norm(BetaVector())))

print(LorentzFactor())