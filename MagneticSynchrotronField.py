from AbstractExternalField import AbstractExternalFieldClass, np, math, scipy
from ParticleBunchClass import ParticleBunch

class MagneticSynchrotronFieldClass(AbstractExternalFieldClass):
    """ Class for generating magnetic fields that increase in magnitude as particles gain momentum

        Class Attributes:
            radius (float): The initial radius that the bunch of particles would have using the 
                initial conditions of the simulation
            initialBField (float): The norm of the initial magnetic field
            magneticfieldStrength (ndarray): Amplitude of magnetic field in 3D space
            angularFrequency (float): Angular frequency of EM field 
            phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
            name (str): Name of EM field
            listOfDimensions (list): List of maximum and minimum dimensions
                of the field in 3D space
    """

    def __init__(self, magneticFieldStrength=np.array([0, 0, 0], dtype=float), particleBunch=ParticleBunch
    , angularFrequency=0.0, phaseShift=0.0, listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Magnetic Synchrotron Field'):
        """ Method inherits the __init__ from the parent class and assigns fieldStrength 
                as magneticFieldStrength to use the GenerateField method in the parent class.
                
            Args:
                magneticfieldStrength (ndarray): Amplitude of electric field in 3D space
                particleBunch (object: ParticleBunch): Bunch of particles that the field increases contains by
                    increasing in magnitude
                angularFrequency (float): Angular frequency of EM field 
                phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
                name (str): Name of EM field
                listOfDimensions (list): List of maximum and minimum dimensions
                    of the field in 3D space
        """
        super().__init__(fieldStrength=magneticFieldStrength, phaseShift=phaseShift
        , angularFrequency=angularFrequency, name=name, listOfDimensions=listOfDimensions)
        self.fieldStrength = magneticFieldStrength
        self.particleBunch = particleBunch
        self.initialBField = np.linalg.norm(self.fieldStrength)
        self.radius = (np.linalg.norm(self.particleBunch.FindBunchMeanMomentum()) 
        / (self.initialBField * self.particleBunch.chargeOfBunch))
        
    def __repr__(self):
        return 'Magnetic Synchrotron Field: {0}, Angular Frequency: {1}, Phase Shift: {2}\
        , Magnetic Field Strength: {3}, Dimensions of the Magnetic Field: {4}'.format(
        self.name, self.angularFrequency, self.phaseShift, self.fieldStrength, self.listOfDimensions)
    
    def ConstantRadius(self):
        """ Method for returning the multiplier of magnetic field strength needed to maintain a 
                fixed radius of bunch oscillation.
            
            Parameters:
                multiplierOfBField (float): Value that the magnetic field must be multiplied by
                    in order to keep the bunch in a fixed radius circular path
            
            Returns:
                multiplierOfBField (float): Value that the magnetic field must be multiplied by
                    in order to keep the bunch in a fixed radius circular path
        """
        multiplierOfBField = (np.linalg.norm(self.particleBunch.FindBunchMeanMomentum())
        / (self.radius * self.particleBunch.chargeOfBunch * self.initialBField))
        return multiplierOfBField

    def GenerateField(self, timeElapsed, affectedParticle):
        """ Method for generating the magnetic field affecting a particle after a certain time.
                Uses an inherited method from the parent class AbstractExternalFieldClass
            
            Args:
                timeElapsed (float): Time that has elapsed in the simulation
                affectedParticle (object: Particle): The particle being affected by the magnetic field
            
            Returns:
                Magnetic Field (ndarray): The magnetic field affecting the particle multipled by
                    the required increase in magnetic field amplitude in order to keep the circular
                    radius of the bunch of particles fixed
        """
        return super().GenerateField(timeElapsed, affectedParticle) * MagneticSynchrotronFieldClass.ConstantRadius(self)