import mido
import numpy as np
import sounddevice as sd

# Constants for audio generation
sample_rate = 44100
duration = 0.2

# MIDI callback function
def midi_callback(message):
    if message.type == 'note_on':
        frequency = 440 * (2 ** ((message.note - 69) / 12))
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        audio = np.sin(2 * np.pi * frequency * t)  # Sawtooth wave generation

        # Play the audio in real-time
        sd.play(audio, sample_rate, device=2)
    elif message.type == 'note_off':
        # Stop playing the audio
        sd.stop()

ports = mido.get_input_names()
print(ports)

port_name = ports[1]
port = mido.open_input(port_name)

# Set the MIDI callback function
port.callback = midi_callback

# Keep the program running
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Close the MIDI port
port.close()