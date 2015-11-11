from functionsfft import *
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('PDCMAP.csv')
time = np.array(data['Time'])
flux = np.array(data['Flux'])
quarter = np.array(data['Quarter'])


newtime, newflux = gap_filler(time, flux)

frequencies, power = fft_complete(newtime, newflux, 1.0)

power = power/np.median(power)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 22}

plt.rc('font', **font)

fig = plt.figure(figsize=(15,8))
ax = fig.add_subplot(1,1,1)
plt.xlim([0.1, 15.0]) 
ax.set_xlabel('Frequency [cycles/day]')
ax.set_ylabel('FFT power')
ax.plot(frequencies, power)
fig.savefig("KOI1169fft.png", dpi = 500)
