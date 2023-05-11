import mido
import sounddevice as sd
import numpy as np
import math
import saw
import time

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

def callback(outdata, frames, time, status):
    outdata[:] = waveform.reshape(-1, 1)

# Global variables
sampling_rate = 44100
buffer_size = 512

# Set up MIDI input
mido.set_backend('mido.backends.rtmidi')  # Use rtmidi backend for MIDI I/O
ports = mido.get_input_names()
input_name = ports[1]  # Replace with the name of your MIDI input device
input_port = mido.open_input(input_name)

# Map notes to their most recent value
active_notes = {}

# Open a stream and start playing the waveform continuously
stream = sd.OutputStream(callback=callback, channels=1, samplerate=sampling_rate, blocksize=buffer_size)
stream.start()

rec = []

# Main loop to receive MIDI messages
try:
    while True:
        for message in input_port.iter_pending():
            midi_callback(message)
        if active_notes:
            waveform = saw.sawtooth(buffer_size/sampling_rate, midi_to_frequency(list(active_notes.keys())[0]), sampling_rate, starting_y=active_notes[list(active_notes.keys())[0]])
            active_notes[list(active_notes.keys())[0]] = waveform[-1]
        else:
            waveform = np.zeros(buffer_size)
        time.sleep(0.01)
        
except KeyboardInterrupt:
    pass

# Stop and close the stream
stream.stop()
stream.close()

# Close the MIDI input connection
input_port.close()
