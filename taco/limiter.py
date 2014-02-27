import time
 
class Speedometer(object):
  def __init__(self):
    self.start = time.time()
    self.last = self.start
    self.rate = 0.0
  
  def add(self,data_len):
    current_time = time.time()
    try:
      self.rate = (self.rate * abs(self.last - self.start) + data_len) / abs(current_time - self.start)
    except:
      self.rate = 0.0
    self.last = current_time
    
    check_time = current_time - 5.0
    
    if self.start < check_time:
      self.start = check_time
    
  def get_rate(self):
    self.add(0)
    return self.rate
