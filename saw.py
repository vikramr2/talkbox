import numpy as np
import math

def starting_saw(starting_y, sampling_rate, frequency):
    period = sampling_rate/frequency
    num_samples = int(period*(1-starting_y)/2)
    time = np.linspace(0, num_samples, num_samples, endpoint=False)
    return (2/period)*time+starting_y

def complete_first_saw(sampling_rate, frequency):
    period = sampling_rate/frequency
    num_samples = int(period/2)
    time = np.linspace(0, num_samples, num_samples, endpoint=False)
    return (2/period)*time-1

def generate_sawtooth_wave(duration, frequency, sampling_rate, phase_shift=0):
    # Calculate the number of samples
    num_samples = int(duration * sampling_rate)
    
    # Calculate the time values for each sample
    time = np.linspace(0, duration, num_samples, endpoint=False)
    
    # Calculate the angular frequency
    angular_frequency = 2 * np.pi * frequency
    
    # Generate the sawtooth wave
    sawtooth_wave = (2 / np.pi) * np.arctan(np.tan(0.5 * angular_frequency * time + phase_shift))
    
    return np.round(sawtooth_wave, 2)

def sawtooth(duration, frequency, sampling_rate, starting_y):
    # Calculate the number of samples
    num_samples = int(duration * sampling_rate)
    
    # Compute first saw
    start = starting_saw(starting_y, sampling_rate, frequency)
    complete = complete_first_saw(sampling_rate, frequency)
    
    # Finish the wave
    len_left = num_samples - len(start) - len(complete)
    finish = generate_sawtooth_wave(len_left/sampling_rate, frequency, sampling_rate)
    
    return np.append(np.append(start, complete), finish)