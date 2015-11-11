import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
import os
import csv

def gap_filler(t, f):
    num_time = len(t) # the original number of data time points (w gaps)
        
    delta_t = t[1:num_time]-t[0:num_time-1] # has a length = len(t) - 2 (bc it ignores endpoints)
    cadence = np.median(delta_t) # what the time interval between points with gaps currently is
    #Fill gaps in the time series (according to 2012 thesis method)
    gap = np.append(np.around(delta_t/cadence), 1).astype(int)
        
    gap_cut = 1.1   #Time differences greater than gap_cut*cadence are gaps    
    gap_loc = [i for i in np.arange(len(gap)) if (gap[i] > gap_cut)]
    num_gap, biggest_gap = len(gap_loc), np.amax(gap) # the number of gaps present 
    
    ################################################################################
    ########## Create a new time and flux array to account for the gaps ############
    ################################################################################
    
    num_cad = sum(gap)  # the number of data points
    time_cad = np.arange(num_cad)*cadence + np.amin(t)
    flux_cad = np.empty(num_cad) 
            
    oldflux_st, newflux_st = 0, 0 # this is an index
    
    for n in np.arange(num_gap):
        oldflux_ed = gap_loc[n]
        gap_sz     = gap[gap_loc[n]]
        newflux_ed = newflux_st + (oldflux_ed-oldflux_st)
        
        flux_cad[newflux_st:newflux_ed] = f[oldflux_st:oldflux_ed]
            
        gap_fill = (np.ones(gap_sz-1))*f[oldflux_ed]
        flux_cad[newflux_ed+1:newflux_ed+gap_sz] = gap_fill
        flux_cad[newflux_ed] = np.mean([flux_cad[newflux_ed-1], flux_cad[newflux_ed+1]])
        
        oldflux_st = oldflux_ed + 1
        newflux_st = newflux_ed + gap_sz    
    
    #account for last part where there is no gap after
    flux_cad[newflux_st:num_cad] = f[oldflux_st:num_time]
    
    return time_cad, flux_cad



def fft_complete(time_cad, flux_cad, extra_fact):
    """ Takes a time array, a series of fluxes, and an oversampling factor and computes the fft
        
    INPUTS: 
        
    time_cad: time array where the flux is obtained
    flux_cad: flux array with flux measurements
    extra_fact: Oversampling factor

        
    OUTPUT:
    
    A flux series that represents the selected model evaluate at t, with a white noise component
    
    freq: Frequencies where the FFT is evaluated, in 1/units of time_cad
    power: The power of the FFT power spectrum
    n: Is the new number of data points, which is equal to 2^(round(log2(N_orig)) + extra_fact), 
        where N_orig is the number of points of time_cad
    bin_sz: is the final distance between consecutive frequencies in the FFT
    peak_width: the expected total width of a peak representing a delta function

    """

    # oversampling
    N = len(time_cad)
    N_log = np.log2(N) # 2 ** N_log = N
    exp = np.round(N_log)
    if exp < N_log:
        exp += 1 #compensate for if N_log was rounded down
    
    newN = 2**(exp + extra_fact)
    n = np.round(newN/N)
    diff = newN - N
    mean = np.median(flux_cad)
    voidf = np.zeros(diff) + mean
    newf = np.append(flux_cad, voidf)
    
    norm_fact = 2.0 / newN # normalization factor 
    f_flux = fft(newf) * norm_fact
        
    freq = fftfreq((len(newf)))
    d_pts = (np.amax(time_cad) - np.amin(time_cad)) / (N-1)
    freq_fact = 1.0 / d_pts #frequency factor 
    freq *= freq_fact
    
    postivefreq = freq > 0 # take only positive values
    freq, f_flux = freq[postivefreq], f_flux[postivefreq]
    
    power = np.abs(f_flux)
    
    bin_sz = 1./len(newf) * freq_fact # distance between consecutive points in cycles per day
    peak_width = 2 * bin_sz * 2**extra_fact #in cycles per day
    return freq, power