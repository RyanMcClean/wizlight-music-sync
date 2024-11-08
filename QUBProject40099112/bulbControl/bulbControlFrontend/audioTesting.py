import pyaudiowpatch as pyaudio
from src.stream_analyzer import Stream_Analyzer
from time import sleep


# p = pyaudio.PyAudio()

# print(p.get_default_wasapi_loopback())

# sleep(20)

ear = Stream_Analyzer(
                    device = 10,                    # Pyaudio (portaudio) device index, defaults to first mic input
                    rate   = 48000,                  # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 60,       # Window size used for the FFT transform
                    updates_per_second  = 500,      # How often to read the audio stream for new data
                    smoothing_length_ms = 50,       # Apply some temporal smoothing to reduce noisy features
                    n_frequency_bins = 51,          # The FFT features are grouped in bins
                    visualize = 0,                  # Visualize the FFT features with PyGame
                    verbose   = True,               # Print running statistics (latency, fps, ...)
                    height    = 0,                  # Height, in pixels, of the visualizer window,
                    window_ratio = 0                # Float ratio of the visualizer window. e.g. 24/9
                    )

# sleep(20)

count = 0
while count < 1000:
    fftx, fft, freqBins, freqAmp = ear.get_audio_features()

    print("Freq:\tAmp:")
    for x in range(len(freqBins)):
        if freqBins[x] < 1000:
            print('%d\t%d' % (freqBins[x], freqAmp[x]))
        else:
            break
    sleep(0.01)
    count += 1
        

