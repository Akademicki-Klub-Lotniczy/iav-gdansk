class SingleSquare:
  def __init__(self, Cord1_X, Cord1_Y, Cord2_X,Cord2_Y,
   Cord3_X,Cord3_Y, Cord4_X,Cord4_Y):
    self.Cord1_X = Cord1_X
    self.Cord1_Y = Cord1_Y
    self.Cord2_X = Cord2_X
    self.Cord2_Y = Cord2_Y
    self.Cord3_X = Cord3_X
    self.Cord3_Y = Cord3_Y
    self.Cord4_X = Cord4_X
    self.Cord4_Y = Cord4_Y
    self.Center_X = (Cord1_X+Cord2_X+Cord3_X+Cord4_X)/4
    self.Center_Y = (Cord1_Y+Cord2_Y+Cord3_Y+Cord4_Y)/4

    self.num_of_measurements = 0
    self.rssi_sum = 0

    def add_rssi(self, rssi_measurement):
      self.rssi_sum+= rssi_measurement   

    @property
    def average_rssi(self):
      if self.num_of_measurements == 0:
        return 0
      
      return self.rssi_sum / self.num_of_measurements