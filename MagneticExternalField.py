from AbstractExternalField import AbstractExternalFieldClass, np, math, scipy

class MagneticExternalFieldClass(AbstractExternalFieldClass):
    """ Class for generating oscillating magnetic fields.

        Class Attributes:
            magneticfieldStrength (numpy array): Amplitude of magnetic field in 3D space
            angularFrequency (float): Angular frequency of EM field 
            phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
            name (str): Name of EM field
            listOfDimensions (list): List of maximum and minimum dimensions
                of the field in 3D space
    """

    def __init__(self, magneticFieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, phaseShift=0.0, listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Magnetic External Field'):
        """ Method inherits the __init__ from the parent class and assigns fieldStrength 
                as magneticFieldStrength to use the GenerateField method in the parent class.
                
            Args:
                magneticfieldStrength (numpy array): Amplitude of electric field in 3D space
                angularFrequency (float): Angular frequency of EM field 
                phaseShift (float): Phase shift of oscillating cosine function (units of 2*pi)
                name (str): Name of EM field
                listOfDimensions (list): List of maximum and minimum dimensions
                    of the field in 3D space
        """
        super().__init__(fieldStrength=magneticFieldStrength, phaseShift=phaseShift
        , angularFrequency=angularFrequency, name=name, listOfDimensions=listOfDimensions)
        self.fieldStrength = magneticFieldStrength
        
    def __repr__(self):
        return 'External Magnetic Field: {0}, Angular Frequency: {1}, Phase Shift: {2}\
        , Magnetic Field Strength: {3}, Dimensions of the Magnetic Field: {4}'.format(
        self.name, self.angularFrequency, self.phaseShift, self.fieldStrength, self.listOfDimensions)
    
    def GenerateField(self, timeElapsed, affectedParticle):
        """ Method for generating the magnetic field affecting a particle after a certain time.
                Uses an inherited method from the parent class AbstractExternalFieldClass
            
            Args:
                timeElapsed (float): Time that has elapsed in the simulation
                affectedParticle (object: Particle): The particle being affected by the magnetic field
            
            Returns:
                Magnetic Field (numpy array): The magnetic field affecting the particle
        """
        return super().GenerateField(timeElapsed, affectedParticle)