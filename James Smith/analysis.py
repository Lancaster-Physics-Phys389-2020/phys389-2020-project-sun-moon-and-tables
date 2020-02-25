from Vis_planet import Planet
import numpy as np
import matplotlib.pyplot as plt
from Vis_accel import Acceleration
from mpl_toolkits import mplot3d
import math
"""This module performs different forms of analysis on simulated planetary data.

The user specifies which .npy file they would like to import and the timestep and method of that file.
Following this, the file is loaded into te analysis module and then the data is sorted into different lists.
The lists are then operated over by the functions inside the analysis module, to fill new lists with values.
These new lists are then operated over by plotting functions to create figures of the data for easy analysis.

    Functions:
        KEFunction(emptyList): Calculate Total Kinetic Energy at a time t
        percentagechangeinKEfunction(emptyList): Calculate % change in total Kinetic Energy at time t
        percentagechangeinpfunction(emptyList): Calculate % change in total Linear Momentum at time t
        percentagechangeinLfunction(emptyList): Calculate % change in total Angular Momentum at time t
        Ufunction(emptyList): Calculate Total Potential Energy at a time t
        PercentagechangeinVirialfunction(emptyList): Calculate % change in Virial Total Energy at a time t
        orbitalPeriod(emptyList): Calculate the orbital period of each body, using Kepler's Law
        figurepositionanalysis(): Plot the orbits of each body
        plotfunction(xlist, ylist, xlabelstring, ylabelstring, linelabel, title): Create a plot and print mean and standard deviation dependent on the list arguments passed to it
        orbitalperiodanalysis(): Plot the orbital periods of each body, using Kepler's law
        orbitalradiusandperiod(emptyList1, emptyList2): Calculate mean and average of the the orbital radii and period of bodies in the system 
    
    Parameters:
        listofbodiesanalysis (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        listofbodiesanalysisx_pos (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        listofbodiesanalysisy_pos (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        listofbodiesanalysisz_pos (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        listofbodiesanalysis_vel (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        listofbodiesanalysisPeriod (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        listofbodiesanalysisradius (list): list of empty lists, number of empty lists equal to the number of bodies in the simulation
        time (list): list empty for appending time entries when loading data1
        data1: .npy file that is loaded to the module
        filename (str): filename of the file to be loaded, passed to data1, without the file extension
        timestep (int): user input of the timestep of the simulation file that was loaded
        method (int): user input of the method of the simulation file that was loaded
        listofbodiesanalysis_KE (list): list empty for appending KE values when peforming KEFunction(emptyList)
        listofbodiesanalysis_percentage_change_KE (list): list empty for appending % change in KE values entries when peforming percentagechangeinKEfunction(emptyList)
        listofbodiesanalysis_percentage_change_p (list): list empty for appending % change in p values entries when peforming percentagechangeinpfunction(emptyList)
        listofbodiesanalysis_percentage_change_L (list): list empty for appending % change in L values entries when peforming percentagechangeinLfunction(emptyList)
        listofbodiesanalysis_U (list): list empty for appending U values when peforming Ufunction(emptyList)
        listofbodiesanalysis_percentage_change_V (list): list empty for appending % change in Total Energy values entries when peforming PercentagechangeinVirialfunction(emptyList)
"""
filename = input("Enter the details of the file you wish to analyse, omitting the file extension. \n \nExample input: Simulation_data_1000.0_50.0_6_1 \n \n")

if filename == "Simulation_data_1000.0_50.0_6_1":
    print("That was an EXAMPLE. Please enter the name of YOUR file. Here, a joke for your troubles. \n \n Two fermions walk into a bar. One says, '' I'll have a bourbon -- neat. '' The other says, '' Damn, that's what I wanted! ''")
#well, you have to have a joke, don't you?
timestep = int(input("Please enter the timestep of the file that you are analysing as an integer, it is the first value after Simulation_data. \nIn the example, you would enter 1000 \n"))
method = int(input("Please enter the method of the file that you are analysing as an integer, it is the final value in the filenmae. \nIn the example, you would enter 1 \n"))
data1 = np.load("%s.npy"%(filename))




listofbodiesanalysis = [[] for planets in data1[0][1]]
listofbodiesanalysisx_pos = [[] for planets in data1[0][1]]
listofbodiesanalysisy_pos = [[] for planets in data1[0][1]]
listofbodiesanalysisz_pos = [[] for planets in data1[0][1]]
listofbodiesanalysis_vel = [[] for planets in data1[0][1]]
listofbodiesanalysisPeriod = [[] for planets in data1[0][1]]
listofbodiesanalysisradius = [[] for planets in data1[0][1]] #this creates the number of lists for the number of planets that we have. [0] access the first entry in data1 and [1] accesses the planet list bit of that first entry. It doesn't matter which entry we check, because the number of planets isn't changing.
time = []


for row in data1: #runs the for loop over each row in data1, allowing us to make lists of our positions and our times with as little code as possible.
    
    time.append(row[0]) #this ensures that we create a full list of all the times, so we have that for any plotting against time that we want to perform!
    
    for entry in range(len(row[1])): #saves all the listofbodies data from their rows, into their respective lists that were generated earlier

        listofbodiesanalysis[entry].append(row[1][entry])

for i in range(len(data1[0][1])): # 0 index refers to the first data entry and 1 index refers to the list of bodies stored for that first entry. So, in the standard case this is 10

    for j in range(len(time)): #ensures that we add values to our lists for every timestep interval, and not putting them in a function leaves them GLOBAL, where they are useful

        listofbodiesanalysisx_pos[i].append(listofbodiesanalysis[i][j].position[0])
        listofbodiesanalysisy_pos[i].append(listofbodiesanalysis[i][j].position[1])
        listofbodiesanalysisz_pos[i].append(listofbodiesanalysis[i][j].position[2])
        listofbodiesanalysis_vel[i].append(listofbodiesanalysis[i][j].velocity)


def KEfunction(emptyList):
    """Calculate the kinetic energy of the system at each time, t. Append each value to a list.
        
        Args:
            emptyList (list): empty list that is then filled with values from the calculation.

        Parameters:
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            holdingVariable (flt): value that is used to iterate over in for loops
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            listofbodiesanalysis_vel (list): provides all velocity data about each body for every timestep saved

        Returns:
            emptyList (list): A now full list of values, that will then be passed to a plot.
    """
    
    for j in range(len(time)):

        holdingVariable = 0.0

        for i in range(len(listofbodiesanalysis)):

            holdingVariable = holdingVariable + 0.5 * listofbodiesanalysis[i][j].mass * np.linalg.norm(listofbodiesanalysis_vel[i][j]) * np.linalg.norm(listofbodiesanalysis_vel[i][j])
        emptyList.append(holdingVariable)


def percentagechangeinKEfunction(emptyList):
    """Calculate the percentage change of energy of the system at each time, t. Append each value to a list.
        
        Args:
            emptyList (list): An empty list that is then filled with values from the calculation.

        Parameters:
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            holdingVariable (flt): value that is used to iterate over in for loops
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            listofbodiesanalysis_vel (list): provides all velocity data about each body for every timestep saved
            first (flt): stores the first value of the calculation to compare against to find percentage change
            current (flt): value appended to emptyList that is the % change in the holdingVariable after the for loop, compared to first

        Returns:
            emptyList (list): A now full list of values, that will then be passed to a plot.
    """    
    holdingVariable = 0.0

    for i in range(len(listofbodiesanalysis)):

        holdingVariable = holdingVariable + 0.5 * listofbodiesanalysis[i][0].mass * np.linalg.norm(listofbodiesanalysis_vel[i][0]) * np.linalg.norm(listofbodiesanalysis_vel[i][0])
    first = holdingVariable

    for j in range(len(time)):

        holdingVariable = 0.0
        current = 0.0
        for i in range(len(listofbodiesanalysis)):

            holdingVariable = holdingVariable + 0.5 * listofbodiesanalysis[i][j].mass * np.linalg.norm(listofbodiesanalysis_vel[i][j]) * np.linalg.norm(listofbodiesanalysis_vel[i][j])
        current = ((holdingVariable - first) / first ) * 100
        emptyList.append(current)


def percentagechangeinpfunction(emptyList):
    """Calculate the percentage change in linear momentum of the system at each time, t. Append each value to a list.
        
        Args:
            emptyList (list): An empty list that is then filled with values from the calculation.

        Parameters:
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            holdingVariable (flt): value that is used to iterate over in for loops
            first (flt): stores the first value of the calculation to compare against to find percentage change
            current (flt): value appended to emptyList that is the % change in the holdingVariable after the for loop, compared to first
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            listofbodiesanalysis_vel (list): provides all velocity data about each body for every timestep saved

        Returns:
            emptyList (list): A now full list of values, that will then be passed to a plot.
    """
    holdingVariable = np.array([0, 0, 0])

    for i in range(len(listofbodiesanalysis)):

        holdingVariable = holdingVariable + listofbodiesanalysis[i][0].mass * listofbodiesanalysis_vel[i][0]
    holdingVariable = np.linalg.norm(holdingVariable)
    first = holdingVariable

    for j in range(len(time)):
        
        holdingVariable = np.array([0, 0, 0])

        for i in range(len(listofbodiesanalysis)):

            holdingVariable = holdingVariable + listofbodiesanalysis[i][0].mass * listofbodiesanalysis_vel[i][j]
        holdingVariable = np.linalg.norm(holdingVariable)
        current = ((holdingVariable - first) / first ) * 100
        emptyList.append(current)


def percentagechangeinLfunction(emptyList):
    """Calculate the percentage change of angular momentum of the system ABOUT THE CENTRE OF MASS OF THE SYSTEM at each time, t. Append each value to a list.
        
        Args:
            emptyList (list): empty list that is then filled with values from the calculation.

        Parameters:
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            holdingVariable1 (ndarray): value that is used to iterate over in for loops
            holdingVariable2 (ndarray): value that is used to iterate over in for loops
            holdingVariable3 (flt): value that is used to iterate over in for loops
            first (flt): stores the first value of the calculation to compare against to find percentage changee change
            centreofmass (flt): value that holds the centre of mass of that timestep of the simulation, to find angular momentum about
            current (flt): value appended to emptyList that is the % change in the holdingVariable after the for loop, compared to first
            listofbodiesanalysis (list): provides data about each body for every timestep saved

        Returns:
            emptyList (list): A now full list of values, that will then be passed to a plot.
    """
    holdingVariable1 = np.array([0, 0, 0])
    holdingVariable2 = np.array([0, 0, 0])
    holdingVariable3 = 0.0
    first = 0.0

    
    for i in range(len(listofbodiesanalysis)):
        #this is for the first centre of mass

        holdingVariable1 = holdingVariable1 + listofbodiesanalysis[i][0].position * listofbodiesanalysis[i][0].mass
        holdingVariable3 = holdingVariable3 + listofbodiesanalysis[i][0].mass
    centreofmass = (holdingVariable1 / holdingVariable3)
    
    for i in range(len(listofbodiesanalysis)):
        #this is for the first angular momentum calculation

        holdingVariable2 = holdingVariable2 +  np.cross( listofbodiesanalysis[i][0].position - centreofmass, listofbodiesanalysis[i][0].mass * listofbodiesanalysis[i][0].velocity )
    first = np.linalg.norm(holdingVariable2)

    for j in range(len(time)):
        #from now on this is now for all the centre of masses and angular momentum calculations
        holdingVariable1 = np.array([0, 0, 0])
        holdingVariable2 = np.array([0, 0, 0])
        holdingVariable3 = 0.0
        current = 0.0

        for i in range(len(listofbodiesanalysis)): 
            #calculates the centre of mass of the system

            holdingVariable1 = holdingVariable1 + listofbodiesanalysis[i][j].position * listofbodiesanalysis[i][j].mass
            holdingVariable3 = holdingVariable3 + listofbodiesanalysis[i][j].mass 
        centreofmass = (holdingVariable1 / holdingVariable3 )


        for i in range(len(listofbodiesanalysis)): 
            #calculates angular momemtum about that centre of mass

            holdingVariable2 = holdingVariable2 + np.cross( listofbodiesanalysis[i][j].position - centreofmass, listofbodiesanalysis[i][j].mass * listofbodiesanalysis[i][j].velocity )
        holdingVariable2 = np.linalg.norm(holdingVariable2)
        current = ((holdingVariable2 - first) / first ) * 100
        emptyList.append(current)


def Ufunction(emptyList):
    """Calculate the potential energy of the system at each time, t. Append each value to a list.
        
        Args:
            emptyList (list): empty list that is then filled with values from the calculation.

        Parameters:
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            holdingVariable1 (flt): value that is used to iterate over in for loops
            holdingVariable2 (flt): value that is used to iterate over in for loops
            G (int): value of the gravitational constant
            disp (ndarray): difference in the position between a body in listofbodies and the current body
            magnitude (flt): magnitude of the numpy array that is disp
            listofbodiesanalysis (list): provides data about each body for every timestep saved

        Returns:
            emptyList (list): A now full list of values, that will then be passed to a plot.
    """
    for j in range(len(time)):

        holdingVariable1 = 0.0
        holdingVariable2 = 0.0
        G = 6.67408e-11

        for i in range(len(listofbodiesanalysis)):
            
            holdingVariable1 = 0.0

            for k in range(len(listofbodiesanalysis)):

                if i == k:
                    continue

                disp = listofbodiesanalysis[i][j].position - listofbodiesanalysis[k][j].position
                
                magnitude = np.linalg.norm(disp)
                
                holdingVariable1 = holdingVariable1 - ((G * listofbodiesanalysis[i][j].mass * listofbodiesanalysis[k][j].mass) / magnitude)
            
            holdingVariable2 = holdingVariable2 + holdingVariable1
        
        emptyList.append(holdingVariable2)


def PercentagechangeinVirialfunction(emptyList):
    """Calculate the Virial conservation of energy of the system at each time, t. Append each value to a list.
        
        Args:
            emptyList (list): empty list that is then filled with values from the calculation.

        Parameters:
            len(time) (int): length of the time list
            index (flt): used to store the value of the total energy of the system at that time t
            listofbodiesanalysis_KE (list): contains all the values for the Kinetic energy of the system at each saved timestep
            listofbodiesanalysis_U (list): contains all the values for the Potential energy of the system at each saved timestep
            current (flt): value appended to emptyList that is the % change in the index after the for loop, compared to index 

        Returns:
            emptyList (list): full list of values, that will then be passed to a plot.
    """
    index = 0.0
    first = 2 * listofbodiesanalysis_KE[0] + listofbodiesanalysis_U[0]
    current = 0.0

    for j in range(len(time)):
        
        index = 2 * listofbodiesanalysis_KE[j] + listofbodiesanalysis_U[j]
        current = ((index - first) / first ) * 100
        emptyList.append(current)



def orbitalPeriod(emptyList):
    """Calculate the orbital period of each body in the simulation using Kepler's Law, about the centre of mass of the system. Append the orbital period to a list.

        Args:
            emptyList (list): empty list that is then filled with values from the calculation.
        
        Parameters:
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            holdingVariable1 (flt): value that is used to iterate over in for loops
            holdingVariable2 (flt): value that is used to iterate over in for loops
            holdingVariable3 (flt): value that is used to iterate over in for loops
            first (flt): value that stores the first value of the calculation to compare against to find percentage change
            centreofmass (flt): value that holds the centre of mass of that timestep of the simulation, to find angular momentum about
            current (flt): value appended to emptyList that is the % change in the holdingVariable after the for loop, compared to first 
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            AstroU (int): 1 Astronomical Unit, used to determine time period of a body in years

        Returns:
            emptyList (list): full list of values, that will then be passed to a plot.
    """
    for j in range(len(time)):

        holdingVariable1 = 0.0
        holdingVariable2 = 0.0
        holdingVariable3 = 0.0
        centreofmass = 0.0
        AstroU = 149597870700

        for i in range(len(listofbodiesanalysis)):
            #calculates the centre of mass of the system
            holdingVariable1 = holdingVariable1 + listofbodiesanalysis[i][j].position * listofbodiesanalysis[i][0].mass
            holdingVariable3 = holdingVariable3 + listofbodiesanalysis[i][0].mass
        centreofmass = (holdingVariable1 / holdingVariable3) 

        for k in range(len(listofbodiesanalysis)):

            holdingVariable2 = math.sqrt( np.linalg.norm((listofbodiesanalysis[k][j].position - centreofmass)/AstroU) * np.linalg.norm((listofbodiesanalysis[k][j].position - centreofmass)/AstroU) * np.linalg.norm((listofbodiesanalysis[k][j].position - centreofmass)/AstroU) )
            emptyList[k].append(holdingVariable2)


def figurepositionanalysis():
    """Produces a 2D plot of the paths of the bodies in the simulation. Saves it as a .png
        
        Parameters:
            listofbodiesanalysisx_pos (list): x positions of all of the bodies in the system
            listofbodiesanalysisy_pos (list): y positions of all of the bodies in the system
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            method (int): method used in the simulation, stated by the user when running the file
            timestep (int): timestep used in the simulation, stated by the user when running the file
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            

        Returns:
            "Method_%s/Figure to show orbits of bodies_%s.png"%(method, timestep): Saves a .png of the graph to the folder destination specified by the user input method and timestep.
    """
    for i in range(len(listofbodiesanalysis)):

        plt.plot(listofbodiesanalysisx_pos[i], listofbodiesanalysisy_pos[i], '-', label = listofbodiesanalysis[i][i].Name )       
    plt.xlabel('x-position (m)')
    plt.ylabel('y-position (m)')
    plt.legend(loc = 1)
    plt.title("Figure to show orbits of bodies")
    plt.savefig("Method_%s/Figure to show orbits of bodies_%s_%s.png"%(method, timestep, len(listofbodiesanalysis)))
    plt.show()

def figurepositionanalysis3d():
    """Generates a 3D plot of the paths of the bodies in the system and saves it as a .png

        Parameters:
            listofbodiesanalysisx_pos (list): x positions of all of the bodies in the system
            listofbodiesanalysisy_pos (list): y positions of all of the bodies in the system
            listofbodiesanalysisz_pos (list): z positions of all of the bodies in the system
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            method (int): method used in the simulation, stated by the user when running the file
            timestep (int): timestep used in the simulation, stated by the user when running the file
        
        Returns:
            "Method_%s/Figure to show 3D orbits of bodies_%s_%s.png"%(method, timestep, len(listofbodiesanalysis)) : Saves a .png of the graph to the folder destination specified by the user input method and timestep. 
    """
    ax = plt.axes(projection = '3d')

    for i in range(len(listofbodiesanalysis)):

        plt.plot(listofbodiesanalysisx_pos[i], listofbodiesanalysisy_pos[i], listofbodiesanalysisz_pos[i], '-', label = listofbodiesanalysis[i][i].Name )

    ax.set_xlabel('x-position (m)')
    ax.set_ylabel('y-position (m)')
    ax.set_zlabel('z-position (m)')
    plt.legend()
    plt.savefig("Method_%s/Figure to show 3D orbits of bodies_%s_%s.png"%(method, timestep, len(listofbodiesanalysis)))
    plt.show()



def orbitalperiodanalysis():
    """Produces a plot of the orbital periods of each of the bodies in the simulation. Saves it as a .png

        Parameters:
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation
            listofbodiesanalysisPeriod (list): list of lists of the orbital periods of the bodies in the simulation
            listofbodiesanalysis (list): provides data about each body for every timestep saved

        Returns:
            "Method_%s/Figure to show orbital period of bodies_%s.png"%(method, timestep)): Saves a .png of the graph to the folder destination specified by the user input method and timestep.
    """
    for i in range(len(listofbodiesanalysis)):
        plt.plot(time, listofbodiesanalysisPeriod[i], '-', label = listofbodiesanalysis[i][i].Name)
    plt.xlabel('Time (s)')
    plt.ylabel('Orbital period (years)')
    plt.legend(loc = 1)
    plt.title('Plot of orbital period of each body about the centre of mass of the system')
    plt.savefig("Method_%s/Figure to show orbital period of bodies_%s.png"%(method, timestep))
    plt.show()

def plotfunction(xlist, ylist, xlabelstring, ylabelstring, linelabel, title):
    """Function that creates a plot from any generalised two lists. Saves it as a .png

        Args:
            xlist (list): values to be the x axis data points
            ylist (list): values to be the y axis data points
            xlabelstring (str): label for the x axis
            ylabelstring (str): label for the y axis
            linelabel (str): label for the data as shown in the legend
            title (str): title of the graph
        
        Parameters:
            method (int): method used in the simulation, stated by the user when running the file
            timestep (int): timestep used in the simulation, stated by the user when running the file

        Returns:
            "Method_%s/%s_%s.png"%(method, title, timestep): Saves a .png of the graph to the folder destination specified by the user input method.
            "Mean of %s is \n%s \nStandard Deviation of %s is \n%s" %( ylabelstring, np.average(ylist), ylabelstring, np.std(ylist) ): Prints the standard deviation and mean of the y axis values.
    """
    plt.plot(xlist, ylist, '-', label = linelabel )       
    plt.xlabel(xlabelstring) 
    plt.ylabel(ylabelstring)
    plt.title("\n%s_\ntimestep%s"%(title, timestep ))
    plt.legend(loc = 1)
    print( "Mean of %s is \n%s \nStandard Deviation of %s is \n%s" %( ylabelstring, np.average(ylist), ylabelstring, np.std(ylist) ) )
    plt.savefig("Method_%s/%s_timestep%s_bodies%s.png"%(method, title, timestep, len(listofbodiesanalysis)  ), bbox_inches='tight')
    plt.show()



def orbitalradiusandperiod(emptyList1, emptyList2):
    """Calculates the mean and standard deviation of orbital radius and orbital period of each body in the system about the Sun.

        Args:
            emptyList1 (list): empty list that is then filled with values from the calculation.  
            emptyList2 (list): A FULL list of values, of the orbital periods that are calculated in orbitalperiodanalysis()
        
        Parameters:
            listofbodiesanalysis (list): provides data about each body for every timestep saved
            len(time) (int): length of the time list
            len(listofbodiesanalysis) (int): length of the list of number of bodies in the simulation

        Returns:
            np.average(emptyList1[i]) (flt): mean of the values in emptyList1
            np.average(emptyList2[i]) (flt): mean of the values in emptyList2
            np.std(emptyList1[i]) (flt): standard deviation of the values in emptyList1
            np.std(emptyList2[i]) (flt): standard deviation of the values in emptyList2
    """
    AstroU = 149597870700

    for j in range(len(time)):

        for i in range(len(listofbodiesanalysis)):
            
            radius = np.linalg.norm((listofbodiesanalysis[i][j].position - listofbodiesanalysis[0][j].position)/AstroU)
            emptyList1[i].append(radius)
    
    for i in range(len(listofbodiesanalysis)):

        print( "Mean radius of %s's orbit is %s (AU) \nWith standard deviation of %s"%(listofbodiesanalysis[i][0].Name, np.average(emptyList1[i]), np.std(emptyList1[i])) )
        print( "\n \n")
    
    for i in range(len(listofbodiesanalysis)):
        
        print("Mean orbital period of %s's orbit is %s (years) \nWith standard deviation of %s"%(listofbodiesanalysis[i][0].Name, np.average(emptyList2[i]), np.std(emptyList2[i])) )
        print("\n \n")

listofbodiesanalysis_KE = []
KEfunction(listofbodiesanalysis_KE)

listofbodiesanalysis_percentage_change_KE = []
percentagechangeinKEfunction(listofbodiesanalysis_percentage_change_KE)

listofbodiesanalysis_percentage_change_p = []
percentagechangeinpfunction(listofbodiesanalysis_percentage_change_p)

listofbodiesanalysis_percentage_change_L = []
percentagechangeinLfunction(listofbodiesanalysis_percentage_change_L)

listofbodiesanalysis_U = []
Ufunction(listofbodiesanalysis_U)

listofbodiesanalysis_percentage_change_V = []
PercentagechangeinVirialfunction(listofbodiesanalysis_percentage_change_V)

orbitalPeriod(listofbodiesanalysisPeriod)

orbitalradiusandperiod(listofbodiesanalysisradius, listofbodiesanalysisPeriod)


print("Your plots will now save to Method_%s/ \nI hope you enjoy them! Oh and have a beer or a glass of wine, you've earned it. \n \n"%(method))
figurepositionanalysis3d()
orbitalperiodanalysis()
figurepositionanalysis()
print("\nI mean it. Wine or beer. 'Tis the season after all! \n")
plotfunction(time, listofbodiesanalysis_percentage_change_L, 'Time (s)', '% change in L (no units)', '% change in L of the system over time', 'Plot of Percentage change in total Angular Momentum over time' )
print("\nyeah. I put print statements for every line here, just to brighten things up a bit. \n")
plotfunction(time, listofbodiesanalysis_percentage_change_KE, 'Time (s)', '% change in KE from initial KE (no units)', '% change in KE of the system over time', 'Plot of Percentage change in Kinetic Energy over time')
print("\nHere's a joke I pulled from reddit. Close the graph to read it \n")
plotfunction(time, listofbodiesanalysis_percentage_change_V, 'Time (s)', '% change of the Total Energy of the system (no units)', '% change of the Total Energy of the system over time', 'Plot of Percentage change of the Total Energy of the system over time' )
print("\nA neutrino walks into a bar but doesn't order anything. He's just passing through. \n \nHere's another physics joke. Close the graph to read it. \n")
plotfunction(time, listofbodiesanalysis_percentage_change_p, 'Time (s)', '% change in p from initial p (no units)', '% change in p of the system over time', 'Plot of Percentage change in Linear Momentum over time' )
print("\nA cop pulled an electron over. 'Do you know how fast you were going?' 'Yes, but now I'm lost.'\n")



