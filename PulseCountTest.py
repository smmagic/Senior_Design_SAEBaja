# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 07:50:21 2018

@author: Alex Snouffer
"""

import time
import pigpio

HALL1 = 5
HALL2 = 6

class hall:
   """
   A class to read a Hall effect sensor.
   """

   def __init__(self, pi, gpio):
      """
      """
      self.pi = pi
      self.gpio = gpio

      self.old_mode = self.pi.get_mode(self.gpio)
      self.pi.set_mode(self.gpio, pigpio.INPUT)
      self.pi.set_pull_up_down(self.gpio, pigpio.PUD_UP)
      self.cb = self.pi.callback(self.gpio)
      self.tally = 0

      self.inited = True

   def pulses(self):
      if self.inited:
         self.tally = self.cb.tally()
      return self.tally

   def cancel(self):
      if self.inited:
         self.inited = False
         self.cb.cancel()
         self.pi.set_mode(self.gpio, self.old_mode)
         
         
DELAY = 0.1
runtime = 10

pi=pigpio.pi()

h1 = hall(pi, HALL1)
h2 = hall(pi, HALL2)

countin = []
countout = []
speed_time = []

inputfile = "inputfile.csv"
outputfile = "outputfile.csv"
timefile = "time.csv"

start = time.time()

while((time.time() - start) <= runtime):
    h1sp = h1.pulses()
    h2sp = h2.pulses()
    time.sleep(DELAY)
    h1ep = h1.pulses()
    h2ep = h2.pulses()
    h1dp = h1ep - h1sp
    h2dp = h2ep - h2sp
    
    timepoint = (time.time() - start)/2
    
    countin.append(h1dp)
    countout.append(h2dp)
    speed_time.append(timepoint)
    
with open(inputfile, "w") as output:
    writer = csv.writer(output, lineterminator = '\n')
    for val in countin:
        writer.writerow([val])
        
with open(outputfile, "w") as output:
    writer = csv.writer(output, lineterminator = '\n')
    for val in countout:
        writer.writerow([val])
        
with open(timefile, "w") as output:
    writer = csv.writer(output, lineterminator = '\n')
    for val in speed_time:
        writer.writerow([val])
        
h1.cancel()
h2.cancel()

pi.stop()
