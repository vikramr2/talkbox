import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import librosa

def stft( input_sound, dft_size, hop_size, zero_pad, window):
    f = []
    for i in range(0, len(input_sound), hop_size):
        if i+dft_size > len(input_sound):
            vec = input_sound[i:]
        else:
            vec = input_sound[i:i+dft_size]
        vec = np.pad(vec, (0, dft_size-len(vec)), 'constant') * np.array(window)
        f.append(np.fft.rfft(vec, n=dft_size+zero_pad))
        
    # Return a complex-valued spectrogram (frequencies x time)
    return np.array(f, dtype=complex)

def istft( stft_output, dft_size, hop_size, zero_pad, window):
    isft = np.fft.irfft(stft_output, n=dft_size+zero_pad) * np.array(window)
    n_frames = len(stft_output)
    x = np.zeros((n_frames-1)*hop_size+dft_size+zero_pad)
    for i in range(n_frames):
        x[i*hop_size:i*hop_size+dft_size+zero_pad] += isft[i]
    # Return reconstructed waveform
    return x

def compute_spectral_envelope(stft_matrix, smoothing_window_size, downsampling_factor):
    # Step 1: Compute the magnitude spectrum
    magnitude_spectrum = np.abs(stft_matrix)

    # Step 2: Smooth the magnitude spectrum
    window = np.ones(smoothing_window_size) / smoothing_window_size
    smoothed_spectrum = np.apply_along_axis(lambda m: np.convolve(m, window, mode='same'), axis=1, arr=magnitude_spectrum)

    # Step 3: Downsample the smoothed spectrum
    downsampled_spectrum = smoothed_spectrum[:, ::downsampling_factor]

    # Step 4: Interpolate the downsampled spectrum
    interpolated_spectrum = np.repeat(downsampled_spectrum, downsampling_factor, axis=1)

    # Step 5: Normalize the spectral envelope
    spectral_envelope = interpolated_spectrum / np.max(interpolated_spectrum)

    return spectral_envelope

def cross_synthesize(modulator, carrier, winsize, hop_size, zero_pad):
    window = np.hanning(winsize)
    modulator_stft = stft(modulator, winsize, hop_size, zero_pad, window)
    carrier_stft = stft(carrier, winsize, hop_size, zero_pad, window)
    print(carrier_stft.shape)
    modulator_envelope = compute_spectral_envelope(modulator_stft, smoothing_window_size=1, downsampling_factor=1)
    carrier_envelope = compute_spectral_envelope(carrier_stft, smoothing_window_size=1, downsampling_factor=1)
    carrier_divided = carrier_stft/carrier_envelope
    vocoded_stft = modulator_envelope * carrier_divided
    window = np.hanning(winsize+zero_pad)
    vocoded = istft(vocoded_stft, winsize, hop_size, zero_pad, window)
    return vocoded