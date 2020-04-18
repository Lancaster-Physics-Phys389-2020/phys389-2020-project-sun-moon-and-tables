from AbstractExternalField import AbstractExternalFieldClass, scipy, np, math

class ElectricExternalFieldClass(AbstractExternalFieldClass):
    """ Class for generating oscillating electric fields.

        Class Attributes:
            electricfieldStrength (ndarray): Amplitude of electric field in 3D space
            angularFrequency (float): Angular frequency of EM field 
            phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
            name (str): Name of EM field
            listOfDimensions (list): List of maximum and minimum dimensions
                of the field in 3D space
    """

    def __init__(self, electricFieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, phaseShift=0.0, listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Electric External Field'):
        """ Constructor for external electric fields.
                Method inherits the __init__ from the parent class and assigns fieldStrength 
                as electricFieldStrength to use the GenerateField method in the parent class.
            
            Args:
                electricfieldStrength (ndarray): Amplitude of electric field in 3D space
                angularFrequency (float): Angular frequency of EM field 
                phaseShift (float): Phase shift of oscillating cosine function (Fraction of a period)
                name (str): Name of EM field
                listOfDimensions (list): List of maximum and minimum dimensions
                    of the field in 3D space
        """
        super().__init__(fieldStrength=electricFieldStrength, phaseShift=phaseShift
        , angularFrequency=angularFrequency, name=name, listOfDimensions=listOfDimensions)
        self.fieldStrength = electricFieldStrength
        
    def __repr__(self):
        return 'External Electric Field: {0}, Angular Frequency: {1}, Phase Shift: {2}\
        , Electric Field Strength: {3}, Dimensions of the Electric Field: {4}'.format(
        self.name, self.angularFrequency, self.phaseShift, self.fieldStrength, self.listOfDimensions)
    
    def GenerateField(self, timeElapsed, affectedParticle):
        """ Method for generating the electric field affecting a particle after a certain time.
                Uses an inherited method from the parent class AbstractExternalFieldClass
            
            Args:
                timeElapsed (float): Time that has elapsed in the simulation
                affectedParticle (object: Particle): The particle being affected by the electric field
            
            Returns:
                Electric Field (ndarray): The electric field affecting the particle
        """
        return super().GenerateField(timeElapsed, affectedParticle)