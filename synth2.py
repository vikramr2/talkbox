import mido
import sounddevice as sd
import numpy as np
import math
import matplotlib.pyplot as plt

def midi_to_frequency(note_number):
    """
    Converts a MIDI note number to its corresponding frequency.
    
    Arguments:
    note_number -- MIDI note number (integer)
    
    Returns:
    frequency -- Frequency in Hertz (float)
    """
    a4_frequency = 440.0  # Frequency of A4 note in Hertz
    
    # Calculate the number of semitones away from A4
    semitones = note_number - 69
    
    # Calculate the frequency using the formula: frequency = a4_frequency * 2^(semitones/12)
    frequency = a4_frequency * math.pow(2.0, semitones / 12.0)
    
    return frequency

# MIDI callback function
def midi_callback(message):
    global active_notes

    if message.type == 'note_on':
        if message.note not in active_notes:
            active_notes[message.note] = 0
    elif message.type == 'note_off':
        if message.note in active_notes:
            del active_notes[message.note]

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

def callback(outdata, frames, time, status):
    outdata[:] = waveform.reshape(-1, 1)

def complete_wave(n, fs, freq):
    period = fs/freq
    return int(math.ceil(n/period)*period-n)

# Global variables
sampling_rate = 44100
buffer_size = 512

# Set up MIDI input
mido.set_backend('mido.backends.rtmidi')  # Use rtmidi backend for MIDI I/O
ports = mido.get_input_names()
input_name = ports[1]  # Replace with the name of your MIDI input device
input_port = mido.open_input(input_name)

# Map notes to how many frames theyve been held for
active_notes = {}

# Open a stream and start playing the waveform continuously
stream = sd.OutputStream(callback=callback, channels=1, samplerate=sampling_rate, blocksize=buffer_size)
stream.start()

rec = []

# Main loop to receive MIDI messages
try:
    while True:
        for note in active_notes:
            active_notes[note] += 1
        for message in input_port.iter_pending():
            midi_callback(message)
        if active_notes:
            waveform = generate_sawtooth_wave(buffer_size/sampling_rate, midi_to_frequency(list(active_notes.keys())[0]), sampling_rate, phase_shift=-complete_wave(buffer_size*active_notes[list(active_notes.keys())[0]], sampling_rate, midi_to_frequency(list(active_notes.keys())[0])))
            print(waveform[0])
        else:
            waveform = np.zeros(buffer_size)
        rec = np.append(rec, waveform)
        
except KeyboardInterrupt:
    pass

# Stop and close the stream
stream.stop()
stream.close()

# Close the MIDI input connection
input_port.close()

plt.plot(rec)
plt.show()