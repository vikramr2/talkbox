CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
LDFLAGS = -L /rtmidi-5.0.0/ -lRtMidi

# Directory containing RtMidi.h
RTMIDI_DIR = rtmidi-5.0.0/

# Source files
SRCS = synth.cpp

# Object files
OBJS = $(SRCS:.cpp=.o)

# Target executable
TARGET = synth

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -I$(RTMIDI_DIR) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
