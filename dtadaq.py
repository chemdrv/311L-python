# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:17:34 2019

@author: mvanstav

This script takes data from two thermocouple circuits, converts voltage to 
temperature, and plots Delta T vs T_sample in real time.
After acquisition is stopped, date is saved to a text file in the same
directory.

"""



import numpy as np
import matplotlib.pyplot as plt
import nidaqmx #Driver to read data from daqboard

# The next two lines are a couple of notes to make sure you're inputting things correctly
# Press enter in the console to move past them

input('!!!Important note!!!!\nYou need to put in your thermocouple calibration data!\nLines 50 and 51 (or close) have space for that!')
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
plt.ylabel(r'$\Delta T$')
plt.title('Press Ctrl+C to exit')

with nidaqmx.Task() as task:
    #I add two channels from the DAQ board to record two voltages
    task.ai_channels.add_ai_voltage_chan('Dev2/ai0')
    task.ai_channels.add_ai_voltage_chan('Dev2/ai1')
    try:
        while True and np.shape(sampleTempArray)[0] < 1200: #Program exits after 20 minutes of acquisition
            # First I read two voltages
            voltage=task.read(number_of_samples_per_channel=1)
            # Next, I store them as temperatures after applying calibration factors
            al2o3Temp = voltage[0][0] * 1 + 0 # Put calibration data here
            sampleTemp = voltage[1][0] * 1 + 0 # Put calibration data here
            # Temperatures get appended to arrays
            al2o3TempArray=np.append(al2o3TempArray,al2o3Temp)
            sampleTempArray=np.append(sampleTempArray,sampleTemp)
            #Plot the data, then pause
            plt.plot(sampleTemp,(al2o3Temp-sampleTemp),'k.')
            plt.draw()
            plt.pause(1/pointsPerSecond)
            
    
    except KeyboardInterrupt:
        print('ending data acquisition')
    
# Here I combine the arrays, transpose them so that they're columns, and save them
# to a user specified filename.
array_for_saving=np.transpose((al2o3TempArray, sampleTempArray))
filename=input('What filename (give an extension) would you like to save to? ')
np.savetxt(filename,array_for_saving,fmt='%8.4f %8.4f',header="T_Al2O3    T_Sample")