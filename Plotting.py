import numpy as np
import pandas as pd
import matplotlib as mpl
import math as math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy 


class PlottingClass:
    """ Class that contains all plotting methods.

        Class Attributes:
            fileName (string): Name of the file that will be used to
                generate plots
            LoadSim (file): Data from the file read by pandas.
    """

    def __init__(self, pickledFile:str):
        """ Constructor for the PlottingClass class.

            Args:
                pickledFile (string): File name of the file that will 
                    be used to generate plots. Exluding file extension
                    and assumes data is saved as a .pkl file.
        """
        self.fileName = pickledFile
        self.LoadSim = pd.read_pickle("%s.pkl"%(pickledFile))

    def ThreeDPositionPlot(self):
        """ Method to generate a 3D plot of position of Particles over time.
        
            Parameters:
                numberOfParticles (int): Number of particles in the simulation
                lengthOfSimulation (int): Number of timesteps that the simulation
                    ran for
                inputData (list): List containing three lists (x, y and z position)
                    for each of the particles in the simulation
            
            Exceptions:
                Attribute Error: If pandas does not detect LoadSim.Simulation, an 
                    attribute error will be raised. This exception prevents the error
                    from triggering and presents no plot.
        """
        try:
            numberOfParticles = len(self.LoadSim.Simulation[0])
            lengthOfSimulation = len(self.LoadSim.Time)
            # creates a list of three lists per particle.
            inputData = [[[], [], []] for i in range(numberOfParticles)]
            for i in range(lengthOfSimulation):
                for j in range(numberOfParticles):
                    for k in range(3):
                        inputData[j][k].append(self.LoadSim.Simulation[i][j].position[k])

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
        """ Method to plot the mean energy of particles in the simulation over time

            Exceptions:
                    Attribute Error: If pandas does not detect LoadSim.Time, an 
                        attribute error will be raised. This exception prevents the error
                        from triggering and presents no plot.
        """
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
        """ Method to plot the standard deviation of the energy of particles in the simulation

            Exceptions:
                Attribute Error: If pandas does not detect LoadSim.Time, an 
                    attribute error will be raised. This exception prevents the error
                    from triggering and presents no plot.
        """
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
        """ Method to plot the velocity of the first particle in the simulation over time

            Parameters:
                lengthOfSimulation (int): Number of timesteps that the simulation
                        ran for
                inputData (list): List containing the norm of the velocity of the first
                    particle in the simulation

            Exceptions:
                    Attribute Error: If pandas does not detect LoadSim.Time, an 
                        attribute error will be raised. This exception prevents the error
                        from triggering and presents no plot.
        """
        try:
            lengthOfSimulation = len(self.LoadSim.Time)
            inputData = []
            for i in range(lengthOfSimulation):
                inputData.append(np.linalg.norm(self.LoadSim.Simulation[i][0].velocity))
                    
            fig = plt.figure()
            plt.plot(self.LoadSim.Time, inputData, label='Velocity Plot baby')
            plt.xlabel("Time (s)"), plt.ylabel("Velocity (ms$^{-1}$)")
            plt.title("figureTitle")
            
            plt.legend()
            # plt.savefig("%s 1st particle velocity.jpg"%(self.fileName))
            plt.show()
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")

    def RadialPhaseChangePlot(self):
        """ Method to create a radial plot of the final standard deviation in energy
                of the particles in each simulation against the phase shift that was
                added to the accelerating field for that simulation.
            
            Exceptions:
                    Attribute Error: If pandas does not detect LoadSim.Phase, an 
                        attribute error will be raised. This exception prevents the error
                        from triggering and presents no plot.
        """
        try:
            fig = plt.polar(self.LoadSim.Phase * 2 * math.pi, self.LoadSim.FinalSpread
            , label='Spread plot baby')
            plt.xlabel("Phase Change as a Fraction of a Period (no units)")
            plt.ylabel("Final Energy Spread Std. (J)")
            plt.title("figureTitle")

            plt.legend()
            # plt.savefig("%s phase change final energy spread.jpg"%(self.fileName))
            plt.show()
        except:
            AttributeError
            print("You cannot plot this figure with the data you have provided.")
        
    def PhaseChangePlot(self, yscale='linear'):
        """ Method to create a plot of the final standard deviation in energy
                of the particles in each simulation against the phase shift that was
                added to the accelerating field for that simulation.
            
            Args:
                yscale (string): Determines the scale of the y axis in the plot
                
            Exceptions:
                    Attribute Error: If pandas does not detect LoadSim.Phase, an 
                        attribute error will be raised. This exception prevents the error
                        from triggering and presents no plot.
        """
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
    
        