class ChargedParticle(Particle):

  def __init__(self, Position=np.array( [0,0,0],dtype =float), Velocity=np.array( [0,0,0],dtype =float), Acceleration=np.array([0, -10,0],dtype =float), Name='Ball', Mass=1.0, Charge=1.0):
    super().__init__(Position=Position, Velocity=Velocity,Acceleration=Acceleration, Name=Name, Mass=Mass)
    self.charge = Charge

    def __repr__(self):
        return 'Charged Particle: {0}, Mass: {1:12.3e}, Charge: {2:12.3e}, Position: {3}, Velocity: {4}, Acceleration: {5}'.format(
        self.Name,self.mass,self.charge,self.position, self.velocity
        ,self.acceleration)
