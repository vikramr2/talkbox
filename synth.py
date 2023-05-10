import mido
import sounddevice as sd
import numpy as np
from pyo import *

# Set up MIDI input
mido.set_backend('mido.backends.rtmidi')  # Use rtmidi backend for MIDI I/O
ports = mido.get_input_names()
input_name = ports[1]  # Replace with the name of your MIDI input device
input_port = mido.open_input(input_name)

# Set up audio parameters
s = Server().boot()
s.start()

# Global variables to store active notes and their associated pyo objects
active_notes = []
active_objects = []

# MIDI callback function
def midi_callback(message):
    global active_notes, active_objects

    if message.type == 'note_on':
        if message.note not in active_notes:
            # Create a new pyo object for the note
            freq = midiToHz(message.note)
            osc = Osc(table=HannTable(), freq=freq, mul=0.3).out()
            active_notes.append(message.note)
            active_objects.append(osc)
        else:
            # If the note is already active, ignore the event
            return

    elif message.type == 'note_off':
        if message.note in active_notes:
            # Release the note if it is active
            index = active_notes.index(message.note)
            obj = active_objects[index]
            obj.stop()
            del active_objects[index]
            del active_notes[index]

# Main loop to receive MIDI messages
try:
    while True:
        for message in input_port.iter_pending():
            midi_callback(message)
except KeyboardInterrupt:
    pass

# Stop and close the pyo server
s.stop()
s.shutdown()

# Close the MIDI input connection
input_port.close()