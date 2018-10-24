# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 09:26:19 2018

@author: Alex Snouffer
"""

import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time, sys, csv

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(7, GPIO.IN)
last_time = time.time()
this_time = time.time()
engine_input = []
speed_time = []
RPM = 0

inputfile = "inputfile.csv"
outputfile = "outputfile.csv"
timefile = "time.csv"

def EventsPerTime(channel):
    global RPM, this_time, last_time, engine_input, speed_time 
    if GPIO.input(channel) > 0.5:
        this_time = time.time()
        RPM = (1/(this_time - last_time))
        engine_input.append(RPM)
        speed_time.append(this_time)
        last_time = this_time
        
GPIO.add_event_detect(7, GPIO.RISING, callback = EventsPerTime, bouncetime = 1)

GPIO.output(11, True)
time.sleep(1)
starttime = time.time()
runtime = 20

while((time.time() - starttime) < runtime):
    time.sleep(0.5)
    
with open(inputfile, "w") as output:
    writer = csv.writer(output, lineterminator = '\n')
    for val in engine_input:
        writer.writerow([val])
        
#with open(outputfile, "w") as output:
#    writer = csv.writer(output, lineterminator = '\n')
#    for val in countout:
#        writer.writerow([val])
        
with open(timefile, "w") as output:
    writer = csv.writer(output, lineterminator = '\n')
    for val in speed_time:
        writer.writerow([val])

print(engine_input)

plt.scatter(speed_time, engine_input)
plt.show()  

    
GPIO.cleanup()
print("Done")