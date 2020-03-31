from AbstractExternalField import AbstractExternalFieldClass, np, math, scipy

class MagneticExternalFieldClass(AbstractExternalFieldClass):
    """ This class will generate an external eagnetic field that can vary
    sinosoidally with time, but each x,y and z currently have the same 
    function. Perhaps some way of changing that on the fly, giving frequency
    as a vector rather than as a float?
    """

    def __init__(self, magneticFieldStrength=np.array([0, 0, 0], dtype=float)
    , angularFrequency=0.0, phaseShift=0.0
    , listOfDimensions = [[-1 * scipy.inf, scipy.inf] for i in range(3)]
    , name='Magnetic External Field'):
        super().__init__(fieldStrength=magneticFieldStrength, phaseShift=phaseShift
        , angularFrequency=angularFrequency, name=name, listOfDimensions=listOfDimensions)
        self.fieldStrength = magneticFieldStrength
        
    def __repr__(self):
        return 'External Magnetic Field: {0}, Angular Frequency: {1}, Phase Shift: {2}\
        , Magnetic Field Strength: {3}, Dimensions of the Magnetic Field: {4}'.format(
        self.name, self.angularFrequency, self.phaseShift, self.fieldStrength, self.listOfDimensions)
    
    def GenerateField(self, timeElapsed, affectedParticle):
        return super().GenerateField(timeElapsed, affectedParticle)