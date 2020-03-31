import numpy as np
import pandas as pd
import matplotlib as mpl
import math as math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy 


class PlottingClass:

    def __init__(self, pickledFile:str):
        self.fileName = pickledFile
        self.LoadSim = pd.read_pickle("%s.pkl"%(pickledFile))

    def ThreeDPositionPlot(self):
        try:
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

        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")
        

    def MeanEnergyPlot(self):
        try:
            fig = plt.figure()
            plt.plot(self.LoadSim.Time, self.LoadSim.Energy, label='Energy Plot baby')
            plt.xlabel("Time (s)"), plt.ylabel("Mean Energy (J)")
            plt.title("figureTitle")

            plt.legend()
            # plt.savefig("%s mean energy.jpg"%(self.fileName))
            plt.show()
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")
        

    def SpreadEnergyPlot(self):
        try:
            fig = plt.figure()
            plt.plot(self.LoadSim.Time, self.LoadSim.Spread, label='Spread Plot baby')
            plt.xlabel("Time (s)"), plt.ylabel("Energy Spread Std. (J)")
            plt.title("figureTitle")

            plt.legend()
            # plt.savefig("%s energy spread.jpg"%(self.fileName))
            plt.show()
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")

    def FirstParticleVelocityPlot(self):
        try:
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
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")

    def RadialPhaseChangePlot(self):
        try:
            fig = plt.polar(self.LoadSim.Phase * 2 * math.pi, self.LoadSim.FinalSpread, label='Spread plot baby')
            plt.xlabel("Phase Change as a Fraction of a Period (no units)"), plt.ylabel("Final Energy Spread Std. (J)")
            plt.title("figureTitle")

            plt.legend()
            # plt.savefig("%s phase change final energy spread.jpg"%(self.fileName))
            plt.show()
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")
        
    def PhaseChangePlot(self, yscale='linear'):
        try:
            fig = plt.figure()
            plt.plot(self.LoadSim.Phase, self.LoadSim.FinalSpread, label='Spread Plot baby')
            plt.xlabel("Phase Change as a Fraction of a Period (no units)"), plt.ylabel("Final Energy Spread Std. (J)")
            plt.title("figureTitle")
            plt.yscale(yscale)
            plt.legend()
            # plt.savefig("%s phase change final energy spread.jpg"%(self.fileName))
            plt.show()
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")
    
        