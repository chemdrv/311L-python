# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:49:37 2019

@author: mvanstav
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import nidaqmx #Driver to read data from daqboard

pointsPerSecond=float(input('How many points per second would you like? '))

timeArray=np.array([])
dataArray=np.array([])
elapsedTime=0

plt.clf()

print('Beginning data acquisition. Press ctrl+c to end')

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan('Dev2/ai0')
    try:
        while True:
            timeArray=np.append(timeArray,time.time())
            elapsedTime=timeArray[-1]-timeArray[0]
            voltage=task.read(number_of_samples_per_channel=1)
            dataArray=np.append(dataArray,task.read(number_of_samples_per_channel=1))
            plt.plot((timeArray-timeArray[0])[-1],dataArray[-1],'k.')
            plt.xlabel('Elapsed time(s)')
            plt.ylabel('Voltage (V)')
            plt.title('Signal acquisition')
            plt.pause(1/pointsPerSecond)
            plt.draw()
    
    except KeyboardInterrupt:
        print('ending data acquisition')
    
plt.plot(timeArray-timeArray[0],dataArray,'.')

plt.draw()

filename = input('What filename would you like the data saved in? Please include the extension in your filename. ')
array_for_saving=np.transpose((timeArray-timeArray[0],dataArray))
np.savetxt(filename, array_for_saving,fmt='%8.4f; %8.4f',header="Time;    Data")