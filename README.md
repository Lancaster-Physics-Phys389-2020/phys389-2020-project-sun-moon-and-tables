# phys389-2020-project-sun-moon-and-tables
phys389-2020-project-sun-moon-and-tables created by GitHub Classroom

Simulating particle accelerators - James Smith - PHYS389 Computer Modelling.

17 python files are used to run the simulation, with all but the main.py file containing a different class required to run a part of the modelling project. 6 further test python test files are included, which can be tested by running pytest on the command line in the main folder of this software.

- How to run this simulation
To run the simulations within this project, run the main.py file. Four simulations are initially included, but the user may comment each simulation out at their own discretion. Simulations in main.py are structured with an initial series of object initialisations, followed by a "# Run conditions ..." line. The methods following the "#Run Conditions ..." line can be commented out to remove a simulation from the main file. As the Conservation Law simulation can be difficult to produce useful results due to the random starting positions of particles in bunches, an set of optional starting conditions for that simulation are available under "# # optional changes ...". These conditions generate a proton, anti-proton pair that oscillate tightly around one another.

* main.py
Launch file that contains four different simulations that can be run and analysed. Run this file to start the simulations.
Cyclotron simulation : Simulates a cyclotron accelerating a bunch of charged particles using a time varying electric field.
Synchrotron Simulation: Simulates a synchotron accelerating a bunch of particles. Uses a time varying magnetic field to keep the radius of the bunch of particles constant, with two constant electric fields at opposite ends of the synchrotron ring to increase the velocity of the bunch.
Phase Change Simulation: Simulates a series of cyclotrons that have time varying electric fields with increasing phase shift added to their sinusoidal function. Shows the best phase shift to reduce the energy spread of the bunch of particles.
Conservation Law Simulation: Simulates a collection of interacting charged particles with no external fields. As a result, conservation of linear momentum, angular momentum and energy of both particles and their fields can be measured.

* Particle.py
Class that creates charged particle objects that interact within the simulations. Objects also generate electromagnetic fields using the PointElectricFieldClass and PointMagneticFieldClass objects. Contains methods for determining total energy, kinetic energy, momentum and relativistic mass.

* ParticleBunchClass.py
Composition class of Particle classes. Creates bunches of Particle objects with a random initial spread in position and in energy. The mean initial position and energy of the bunch can also be specified. Generally used as a composition of Particle objects for applying methods to all particles in the simulation.

* AbstractExternalField.py
Abstract base class for all external fields. Defines methods that any child class that is an external field must have. __repr__() is an abstract method required for child classes, and GenerateField() and IsParticleInField() are methods inherited by child classes. This saves defining these methods in every child class. GenerateField() calculates the electric or magnetic field produced by a sinusoidal wavefunction with specified angular frequency, phase shift and amplitude. IsParticleInField() determines if the particle's position is within the boundaries of the electromagnetic field in order to determine if a field acts on a particle.

* AbstractPointField.py
Abstract base class for all point originating fields. Defines methods that any child class that is a point originating field must have.
__repr__() is an abstract method required for child classes as is GenerateField() since the functions for electric and magnetic fields from point particles are different.

* AbstractSimulation.py
Abstract base class for all simulations. Defines methods that any child class that is a simulation must have.
RunSimulation() and SaveSimulation() are abstract methods required for child classes. These methods are required to run and save any simulation although additional methods may be added for complex simulations.

* GenericField.py
Parent class for all fields in a simulation; AbstractExternalField and AbstractPointField.

* ElectricExternalField.py
Child class of AbstractExternalField. Creates an external electric field, inheriting IsParticleInField() and GenerateField() methods from the AbstractExternalFieldClass in order to determine if a particle is inside of its dimensions and the magnitude of the field.

* MagneticExternalField.py
Child class of AbstractExternalField. Creates an external magnetic field, inheriting IsParticleInField() and GenerateField() methods from the AbstractExternalFieldClass in order to determine if a particle is inside of its dimensions and the magnitude of the field.

* MagneticSynchrotronField.py
Child class of AbstractExternalField. Creates an external magnetic field that increases in magnitude as the bunch of particles in the simulation increases in linear momentum. Inherits IsParticleInField() and GenerateField() methods from the AbstractExternalFieldClass. ConstantRadius() returns the increase in magnitude in the magnetic field required for the radius of circular path of the particle bunch to reamin constant as the momentum of the bunch increases.

* PointElectricField.py
Child class of AbstractPointField. Generates an electric field that originates from a point-like particle. GenerateField() method takes the the affected Particle object as an argument and this class is called by the source Particle object. 

* PointMagneticField.py
Child class of AbstractPointField. Generates an magnetic field that originates from a point-like particle. GenerateField() method takes the the affected Particle object as an argument and this class is called by the source Particle object. 

* SumEMFields.py
Composition class of ParticleBunch, MagneticExternalField and ElectricExternalField classes. SumOfEMFields() method returns the sum of the electromagnetic fields from interacting particles and external time varying electromagnetic fields. GiveAcceleration() method applies the Lorentz force on a Particle object with the electric and magnetic field components returned from SumOfEMFields(). The relativistic mass of the particle is used to determine the acceleration provided by the electromagnetic fields.

* Plotting.py
Class that contains methods to generate different plots depending on the .pkl file that is provided as an argument. 
ThreeDPositionPlot() produces a plot of the positions of particles in the simulation in three dimensions.
MeanEnergyPlot() produces a figure that shows the mean energy of the bunch over time.
SpreadEnergyPlot() produces a figure that shows the standard deviation of the energy of the particle bunch over time.
MeanParticleVelocityPlot() produces a figure that shows the norm of the mean velocity of the particle bunch over time.
RadialPhaseChangePlot() generates a figure of the final standard deviation of energy of the bunch of particles across a series of simulations with accelerating electric fields of different phases. Displayed as a polar plot with the phase shift as the angular axis and standard deviation as the radial axis.
PhaseChangePlot() generates a figure of the final standard deviation of energy of the bunch of particles across a series of simulations with accelerating electric fields of different phases.
ConservationOfMomentumPlot() produces a plot of the norm of the total momentum of particles in the simulation over time.
ConservationOfEnergyFieldsPlot() produces a plot of the potential energy in the electromagnetic fields in the simulation over time.
ConservationOfEnergyParticlesPlot() produces a plot of the kinetic energy of particles in the simulation over time.
ConservationOfAngularMomentumPlot() produces a plot of the norm of the total angular momentum of particles in the simulation over time.

* SimulationStandard.py
Child class of AbstractSimulationClass. Runs a standard simulation with external electromagnetic fields and interacting particles. Simulation is run with the RunSimulation() method and saved to a .pkl file with the SaveSimulation() method that are required due to the parent AbstractSimulationClass.

* SimulationPhaseChange.py
Child class of AbstractSimulationClass. Runs several simulations with the same starting conditions. In the simuations, the accelerating electric field that acts on the particle bunch has a phase shift added to it. Saved data can then be used to determine the ideal phase shift in order to reduce the spread in energy of particles in the bunch. Simulation is run with the RunSimulation() method and saved to a .pkl file with the SaveSimulation() method that are required due to the parent AbstractSimulationClass.

* SimulationConservationLaws.py
Child class of AbstractSimulationClass. Runs a simulation that does not allow external electromagnetic fields. As a result, the conservation of angular momentum, linear momentum and total energy can be measured quantitatively. Simulation is run with the RunSimulation() method and saved to a .pkl file with the SaveSimulation() method that are required due to the parent AbstractSimulationClass.

* test_Particle.py
Contains pytest functions for testing the performance of functions in the Particle file.

* test_ParticleBunch.py
Contains pytest functions for testing the performance of functions in the ParticleBunchClass file.

* test_ExternalFieldFiles.py
Contains pytest functions for testing the performance of functions in the: GenericField, AbstractExternalField, ElectricExternalField, MagneticExternalField and MagneticSynchrotronField files.

* test_PointFieldFiles.py
Contains pytest functions for testing the performance of functions in the: AbstractPointField, PointElectricField and PointMagneticField files.

* test_SumEMFields.py
Contains pytest functions for testing the performance of functions in the the SumEMFields file.

* test_Simulations.py
Contains pytest functions for testing the performance of functions in the: AbstractSimulation, SimulationStandard, SimulationPhaseChange and SimulationConservationLaws files.
