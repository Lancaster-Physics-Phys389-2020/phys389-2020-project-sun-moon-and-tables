from AbstractExternalField import AbstractExternalFieldClass, scipy, np, math

class ElectricExternalFieldClass(AbstractExternalFieldClass):
    """ This class will generate an external electric field that can vary
    sinosoidally with time, but each x,y and z currently have the same 
    function. Perhaps some way of changing that on the fly, giving frequency
    as a vector rather than as a float?
    """

    def __init__(self, electricFieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0
    , listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Electric External Field'):
        super().__init__(fieldStrength=electricFieldStrength
        , angularFrequency=angularFrequency, name=name, listOfDimensions=listOfDimensions)
        self.fieldStrength = electricFieldStrength
        self.angularFrequency = angularFrequency
        self.name = name
        self.listOfDimensions = listOfDimensions
        
    def __repr__(self):
        return 'Field Name: {0}, Angular Frequency: {1}, Electric Field Strength: {2}\
            Dimensions of the Electric Field: {3}'.format(self.name
            , self.angularFrequency, self.fieldStrength, self.listOfDimensions)
    
    def generateField(self, timeElapsed, affectedParticle):
        return super().generateField(timeElapsed, affectedParticle)