import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy 


class PlottingClass:

    def __init__(self, pickledFile:str):
        self.fileName = pickledFile
        self.LoadSim = pd.read_pickle("%s.pkl"%(pickledFile))

    def ThreeDPositionPlot(self):
        numberOfParticles = len(self.LoadSim.Simulation[0])
        lengthOfSimulation = len(self.LoadSim.Time)
        inputData = [[[], [], []] for i in range(numberOfParticles)]
        # creates a list per particle.
        for i in range(lengthOfSimulation):
            for j in range(numberOfParticles):
                for k in range(3):
                    inputData[j][k].append(self.LoadSim.Simulation[i][j].position[k])
                    # so this is the one line that does position. could swap this out
                    # for different simulation properties.

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for j in range(numberOfParticles):
            ax.plot(inputData[j][0], inputData[j][1], inputData[j][2]
            , label='%s'%(self.LoadSim.Simulation[0][j].name))
        plt.title("figureTitle")
        ax.set_xlabel("x position (m)"), ax.set_ylabel("y position (m)"), ax.set_zlabel("z position (m)")

        ax.legend()
        # plt.savefig("%s 3D position.jpg"%(self.fileName))
        plt.show()

    def MeanEnergyPlot(self):
        fig = plt.figure()
        plt.plot(self.LoadSim.Time, self.LoadSim.Energy, label='Energy Plot baby')
        plt.xlabel("Time (s)"), plt.ylabel("Mean Energy (J)")
        plt.title("figureTitle")

        plt.legend()
        # plt.savefig("%s mean energy.jpg"%(self.fileName))
        plt.show()

    def SpreadEnergyPlot(self):
        fig = plt.figure()
        plt.plot(self.LoadSim.Time, self.LoadSim.Spread, label='Spread Plot baby')
        plt.xlabel("Time (s)"), plt.ylabel("Energy Spread Std. (J)")
        plt.title("figureTitle")

        plt.legend()
        # plt.savefig("%s energy spread.jpg"%(self.fileName))
        plt.show()

    def FirstParticleVelocityPlot(self):
        numberOfParticles = len(self.LoadSim.Simulation[0])
        lengthOfSimulation = len(self.LoadSim.Time)
        inputData = []
        for i in range(lengthOfSimulation):
            inputData.append(np.linalg.norm(self.LoadSim.Simulation[i][0].velocity))
                
        fig = plt.figure()
        plt.plot(self.LoadSim.Time, inputData, label='Velocity Plot baby')
        plt.xlabel("Time (s)"), plt.ylabel("Velocity (m$^{-1}$)")
        plt.title("figureTitle")
        
        plt.legend()
        # plt.savefig("%s 1st particle velocity.jpg"%(self.fileName))
        plt.show()