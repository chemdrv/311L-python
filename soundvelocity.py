import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import rfft, fftfreq, irfft
import sounddevice as sd
from scipy.io import wavfile

# Collecting user input

fileroot = input('What filename do you wish to use? No extension: ')
filename = fileroot + ".txt"
datafile = fileroot + ".wav"
collecttime = float(input('How long do you want to collect data? (in seconds)'))
sampfreq = 44100



message = input("Press enter when you're ready to begin data acquisition")
print("Beginning acquisition")
recording = sd.rec(int(collecttime * sampfreq),channels=1)

sd.wait()
print("Acquisition complete")
wavfile.write(filename,sampfreq,recording)

freq,Signal = wavfile.read(filename)

# Fourier transform calculates a frequency spectrum
# for a signal in the time domain
# Use Discrete Fourier transform to get signal from time to frequency domain

# number of samples in recording
N = int(sampfreq*collecttime)

raw = np.fft.rfft(Signal)
yf = np.real(raw*np.conj(raw))
xf = np.fft.rfftfreq(N, 1 / sampfreq)

plt.clf()
plt.plot(xf, yf, linewidth=1, label='after fourier transform')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.xlim([0, 5000])
plt.legend()
plt.show()

#now the data is shown in the magnitude
#want to remove the other sounds lower than the desired ones
#will need to experimentally detemine how much 'noise' needs to be filtered

#Now we begin filtering oiut values below 300 
#300 is an arbitrary number created for the sample signals, will need to be adjusted
#any frequencies below this set amunt will be filtered out

#identifying data points within the sample where the minimum frequency is satisfied
#indices = yf_abs>10000
#creating new variable which will hold all the data points from the sample which meet the requirements
#yf_Clean = indices * yf
#xf_Clean = indices * xf
# Inverse back to time signal showing only the constructive signals
#ConstructiveFreq = irfft(yf_Clean)
# plotting constructive signal versus time 
#plt.plot(xf_Clean,yf_Clean,linewidth=1,label="cleaned up")
#plt.legend()
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.show()

combinedArray = np.column_stack((xf,yf))
np.savetxt(datafile,combinedArray,fmt='%10.4f; %10.4f',header=r'frequency;Average db')



