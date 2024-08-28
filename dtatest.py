# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:29:59 2019

@author: mvanstav

This is a test script for differential thermal analysis, and very similar to the data
acquisition script 'dtadaq.py'.
Major changes: it plots T_al2o3 vs T_sample and omits saving because that's not necessary.

To test your setup:

1. Leave both thermocouples in air
2. Enter calibration data into this program
3. Start this program
4. Do you see what you expect on the plot?
5. Hold your hand over one sample thermocouple. Then place it ice.
Then back to air. Do you see what you expect on the plot?
6. Repeat step 5 with the other thermocouple.

If the plot becomes too crowded during testing, you can X the figure window.
It'll reopen blank and continue from there.
Use the temperature response you see to guide your troubleshooting.
"""



import numpy as np
import matplotlib.pyplot as plt
import nidaqmx #Driver to read data from daqboard
import keyboard

# The next two lines are a couple of notes to make sure you're inputting things correctly
# Press enter in the console to move past them

input('!!!Important note!!!!\nYou need to put in your thermocouple calibration data!\nLines 62 and 63 (or close) have space for that!')
input('AI1 should be into the sample mixture.\nAI0 should be into the aluminum oxide')

# I've hard coded the acquisition rate because this is a good rate for this experiment.
# But change it if you like.
#pointsPerSecond=float(input('How many points per second would you like? '))
pointsPerSecond=1

# Here I initialize two arrays to store the temperatures
al2o3TempArray=np.array([])
sampleTempArray=np.array([])

#Setting up the plot
plt.clf()
plt.xlabel(r'$T_{sample}$')
plt.ylabel(r'$T_{Al2O3}$')
plt.title('Press Ctrl+C to exit')

print("Beginning test loop. Hold 'd' to exit")

with nidaqmx.Task() as task:
    #I add two channels from the DAQ board to record two voltages
    task.ai_channels.add_ai_voltage_chan('Dev2/ai0')
    task.ai_channels.add_ai_voltage_chan('Dev2/ai1')
    while True:
        # First I read two voltages
        voltage=task.read(number_of_samples_per_channel=1)
        # Next, I store them as temperatures after applying calibration factors
        al2o3Temp = voltage[0][0] * 1 + 0 # Put calibration data here
        sampleTemp = voltage[1][0] * 1 + 0 # Put calibration data here
        # Temperatures get appended to arrays
        al2o3TempArray=np.append(al2o3TempArray,al2o3Temp)
        sampleTempArray=np.append(sampleTempArray,sampleTemp)
        #Plot the data, then pause
        plt.plot(sampleTemp,al2o3Temp,'k.')
        plt.draw()
        plt.pause(1/pointsPerSecond)
        if keyboard.is_pressed("d"):
            print("Ending test loop")
            break
            
    
