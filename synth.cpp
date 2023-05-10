#include <iostream>
#include <cstdlib>
#include <chrono>
#include <thread>
#include <signal.h>
#include "rtmidi-5.0.0/RtMidi.h" // Include the RtMidi header file

// MIDI callback function
void midiCallback(double timestamp, std::vector<unsigned char> *message, void *userData)
{
    // Handle incoming MIDI messages
    unsigned int nBytes = message->size();
    std::cout << "Received MIDI message: ";
    for (unsigned int i = 0; i < nBytes; i++) {
        std::cout << static_cast<int>((*message)[i]) << " ";
    }
    std::cout << std::endl;
    // Add your code here to process the MIDI message
}

// Signal handler for termination
void sigintHandler(int signum)
{
    // Clean up resources and exit gracefully
    std::cout << "Exiting..." << std::endl;
    exit(signum);
}

int main()
{
    // Register the signal handler for termination (Ctrl+C)
    signal(SIGINT, sigintHandler);

    try {
        // Create an instance of RtMidiIn
        RtMidiIn midiin;

        // Set the MIDI callback function
        midiin.setCallback(&midiCallback);

        // Open the MIDI input port (replace with the appropriate port number or name)
        midiin.openPort(0);

        // Ignore any sysex, timing, or active sensing messages
        midiin.ignoreTypes(true, true, true);

        // Main loop
        while (true) {
            // Do any other processing here
            // ...
            
            // Sleep for a short duration to reduce CPU usage
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
        }
    } catch (RtMidiError &error) {
        // Handle any RtMidiError that might occur
        error.printMessage();
        return 1;
    }

    return 0;
}
