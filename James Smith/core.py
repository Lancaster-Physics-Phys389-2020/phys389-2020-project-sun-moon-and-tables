from Vis_planet import Planet
import numpy as np
from Vis_accel import Acceleration
import copy
import time
"""This is the core module, that instanciates the bodies that you wish to simulate and then imports the Acceleration and Planet classes to simulate the system.
    The simulation data is then saved to a .npy file so that analysis can be done on the data in a separate module.

    Parameters:
        methodChoice (int): user input method that is supplied to Planet.update to update the simulation. 0 or 1.
        deltaT (flt): user input timestep of the simulation.
        SaveLength (flt):  User input duration of the simulation, in years.
        listofbodies (list): list of Planet instances that can be added to to create a more complex simulation.
        Date (str): Date that the data was saved, to help the user should they wish to add more bodies.
        """
methodChoice = int(input('What method would you like to use? \nEuler Cromer = 1 \nEuler Forward = 2 \n'))

if methodChoice != 1 and methodChoice != 2: #inserts the choice of method into the planet instances.
    raise ValueError('You must choose a valid method option, 1 or 2. YA DINGUS!')

Sun = Planet([0.,0.,0.],[0.,0.,0.],[0.,0.,0.],'Sun',1.988500e30, methodChoice)
Earth = Planet([1.394719549832620E+11 ,-5.789826155025420E+10 ,-2.278791476268321E+07], [ 1.093569656371002E+04 , 2.738934703721208E+04 , 2.460760934280160E-00],[0.,0.,0.],'Earth',5.972e24, methodChoice)
Jupiter = Planet([1.118978284994411E+11 , 7.540076418631721E+11 ,-5.607436984309971E+09], [-1.308832107446669E+04 , 2.529407021440497E+03 , 2.828793718737928E+02],[0.,0.,0.],'Jupiter',1.898e27, methodChoice)
Moon = Planet([1.398569161985322E+11 ,-5.789857045278046E+10 , 7.361336727492511E+06],[ 1.099310357076541E+04 , 2.840863778324828E+04 ,-8.487927455405853E+01],[0,0.,0.],'Moon',7.348e22, methodChoice)
Mercury = Planet([4.707963346863978E+10 ,-3.815766881789985E+10 ,-7.439855155565299E+09],[ 2.105780444070472E+04 , 4.012799400097397E+04 , 1.342826699635642E+03],[0.,0.,0.],'Mercury',3.285e23, methodChoice)
Mars = Planet([1.415775398593754E+11 , 1.688060528962781E+11 , 4.789545247670263E+07],[-1.763768924143767E+04 , 1.762947766322560E+04 , 8.035507902014567E+02],[0,0,0],'Mars', 6.39e23, methodChoice)
Venus = Planet([3.731241827150682E+10 , 1.011930373421612E+11 ,-7.775745053192601E+08],[-3.297558973537696E+04 , 1.195073488058969E+04 , 2.066606738674702E+03],[0,0,0],'Venus',4.867e24, methodChoice)
Neptune = Planet([-1.127371677217944E+12 ,-4.387056492047895E+12 , 1.163216339247293E+11], [ 5.216506363443592E+03 ,-1.321923817441395E+03 ,-9.341450987632016E+01],[0,0,0],'Neptune',1.024e26, methodChoice)
Saturn = Planet([-1.072561665065800E+12 , 8.579852275834795E+11 , 2.762206068652129E+10],[-6.568572760350163E+03 ,-7.568669861600487E+03 , 3.931448335114762E+02],[0,0,0],'Saturn',5.683e26, methodChoice)
Uranus = Planet([-2.079300036477388E+12 ,-1.846467843843178E+12 , 2.012517306226528E+10],[ 4.458663790428338E+03 ,-5.409096864602689E+03 ,-7.776468467380493E+01],[0,0,0],'Uranus',8.681e25, methodChoice)
Pluto = Planet([-4.223460714423923E+12 ,-1.064449902363150E+12 , 1.335506859479291E+12],[ 2.050110885842706E+03 ,-5.609451568935953E+03 , 2.552084630377038E+01], [0,0,0], 'Pluto', 1.307e22, methodChoice)
Voyager2 = Planet([1.414989569929121E+11,-4.986270721380867E+10,2.807031619079942E+09], [1.319155486230084E+04, 3.660529798684437E+04, 3.209519610826694E+03], [0, 0, 0], 'Voyager2', 721.9, methodChoice)

Date = "1977-Aug-30 15:33:00.0000"

listofbodies = [Sun, Earth, Jupiter, Moon, Mercury, Mars, Venus, Neptune, Saturn, Uranus, Voyager2, Pluto] #the list of bodies that will be supplied to the Acceleration class
SaveLength = float(input("How long do you want the simulation to run for? (in years) \n"))
deltaT =  float(input("With what time step? (in seconds) \n")) #timestep of the update function in the Planet class

def runsimulation(methodChoice, deltaT, SaveLength, listofbodies):
    """Take user input data to create an N-body gravitational system simulation over time.
    Import Planet and Acceleration classes to perform acceleration calculations and update the parameters of each Planet instance corresponding to the calculations.
    Update Planet instances respective to the method that the user inputs, applied in the Planet class.
    Deepcopy and append simulation data to a list (dataList) and save this list to a .npy file, named as per the conditions set by the user.
    Print loading information to the terminal for the user, for helpful assistance and information.

    Args:
        methodChoice (int): user input method that is supplied to Planet.update to update the simulation. 0 or 1.
        deltaT (flt): user input timestep of the simulation.
        SaveLength (flt):  User input duration of the simulation, in years.
        listofbodies (list): list of Planet instances that can be added to to create a more complex simulation.

    Parameters:
        Darren (int): Current percentage complete for the loading bar
        SimLength (int): converts number of years of SaveLength in seconds and stores it
        start1 (flt): time at the start of the simulation
        start2 (flt): time at the end of the simulation
        loadingtimeiteration (flt): time at that current iteration of saving data in the simulation
        timetaken (flt): difference in loadingtimeiteration and start1
        t (flt): float that is added to every deltaT by deltaT during the simulation, saved
        dataList (list): empty list that data will be appended to during the simulation
        Solar (Planet): Instance of the Acceleration class that will calculate the accelerations of each body due to N-1 other bodies in an N body system

    Returns:
        dataList (list): list of times and Planet instances for that time, saved every once every 50 updates to the system
        "Simulation_data_%s_%s_%s_%s"%(deltaT, SaveLength, len(listofbodies), methodChoice), dataList): Saves a npy file with name based on the arguments given to the function
        timeremaining (int): Printed to the terminal stating the estimated time remaining for the simulation to compelete
        duration (flt): Total time it took for the simulation to run
        Darren (int): Current percentage complete

    Raises:
        ValueError: if deltaT > SimLength
        ValueError: if deltaT or SimLength < 0
        ValueError: if listofbodies < 2
    """
    SimLength = 365 * 86400 * SaveLength #converts the value put in as the duration into years, using the user value SaveLength

    if deltaT > SimLength: #just checks that the duration is less than the timestep
        raise ValueError("Use a proper timestep, timestep must be less than the total duration of the simulation!")
    if deltaT <= 0 or SimLength <= 0:
        raise ValueError("Use a proper timestep and duration, you can't have a negative time! TRY AGAIN, CODE BREAKER!")
    if len(listofbodies) < 2:
        raise ValueError("You need at least two bodies in your simulation! What's the point of simulating one body? Try again bud.")

    start1 = time.time() #tells the user how long the simulation took, for bragging rights against other coders

    Solar = Acceleration(listofbodies) #instanciates*(spelling) the Acceleration class with the list of bodies
    t = 0.0 #this is for time
    dataList = [] #an empty list for our data to go into later
    Darren = 0 #my cheeky variable name to make my loading bar work

    for t in np.arange (0.0, SimLength, deltaT): #runs over the specified length of the simulation, with the specified timestep

        t += deltaT
        Solar.accelMethod() #for every period, run the update method for the solar instance of the acceleration class
        
        for i in range(len(listofbodies)): 
        
            listofbodies[i].update(deltaT)
        
        if t % (50 * deltaT) == 0.0: #saves every 50th period to the file
            
            item = [t, copy.deepcopy(listofbodies)]
            dataList.append(item)
        
        if int(t*100.0/SimLength) > Darren: #prints the percentage complete string for running a simulation
            
            Darren=int(t*100.0/SimLength) #sets the value of Darren to the pecentage that the code has competed so far
            loadingtimeiteration = time.time() 
            timetaken = loadingtimeiteration - start1 #determines the time taken so far
            timeremaining = timetaken * (100 / Darren) - timetaken #calculates the time remaining for the simulation to complete
            print("%s%% Complete, Time Remaining %s seconds \n"%(Darren, round(timeremaining)))

    print('\n')

    np.save("Simulation_data_%s_%s_%s_%s"%(deltaT, SaveLength, len(listofbodies), methodChoice), dataList) #saves the data with a useful format: time interval, total number of years, number of bodies and the method choice

    start2 = time.time() #ends the time after we save, to maintain honour when competing agains other simulations
    duration = start2 - start1

    print('That took %s seconds! Enjoy your file and have a nice day!\n \n'%(duration)) #manners maketh the man
    print('Your file is saved as Simulation_data_%s_%s_%s_%s.npy \n'%(deltaT, SaveLength, len(listofbodies), methodChoice)) #this is just fecking helpful, means you can copy and paste it

    print('\nFor use in the analysis file, you will need the name of the file, without the file extension. I suggest you copy this! \n \nSimulation_data_%s_%s_%s_%s \n \n'%(deltaT, SaveLength, len(listofbodies), methodChoice))

runsimulation(methodChoice, deltaT, SaveLength, listofbodies) #runs the simulation. *shocker*