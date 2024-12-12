"""File for syncronising the audio beat with the music
being played through the specified audio device
"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

try:
    import pyaudiowpatch as pyaudio
except ImportError:
    import pyaudio

from time import sleep, time

try:
    from .Realtime_PyAudio_FFT.src.stream_analyzer import Stream_Analyzer
    from .Realtime_PyAudio_FFT.src.stream_reader_pyaudio import Stream_Reader
except ImportError:
    from Realtime_PyAudio_FFT.src.stream_analyzer import Stream_Analyzer
    from Realtime_PyAudio_FFT.src.stream_reader_pyaudio import Stream_Reader
try:
    from helpers import send_udp_packet
except ModuleNotFoundError:
    from .helpers import send_udp_packet


def beat(ip, packet):
    print("\nbeat\n")
    send_udp_packet(ip, packet=packet)


def getWorkingDeviceList():
    devices = []
    pa = pyaudio.PyAudio()
    device_count = pa.get_device_count()
    for num in range(device_count):
        device = pa.get_device_info_by_index(num)
        if device["maxInputChannels"] > 0:
            devices.append(
                {"num": device["index"], "name": device["name"], "maxInputChannels": device["maxInputChannels"]}
            )
    return devices


def main(device=None):
    ip = "192.168.50.128"
    packet = "turn_to_full"

    ear = Stream_Analyzer(
        # Pyaudio (portaudio) device index, defaults to first mic input
        device=device,
        rate=None,  # Audio samplerate, None uses the default source settings
        FFT_window_size_ms=60,  # Window size used for the FFT transform
        updates_per_second=250,  # How often to read the audio stream for new data
        smoothing_length_ms=100,  # Apply some temporal smoothing to reduce noisy features
        n_frequency_bins=150,  # The FFT features are grouped in bins
        visualize=False,
        verbose=True,
    )

    send_udp_packet(ip, packet="turn_on", attempts=5)

    bufferSize = 100

    freqArray = {}

    tempLow = []
    tempMid = []
    tempHigh = []

    for x in range(bufferSize):
        fftx, fft, freqBins, freqAmp = ear.get_audio_features()
        low = 0
        mid = 0
        high = 0
        for i, x in enumerate(freqBins):
            # if x.item() < 129:
            #     freqArray.setdefault(x.item(), []).append(freqAmp[i].item() if freqAmp[i].item() != 0 else 1)
            if x.item() < 43:
                low += x.item()
            elif x.item() < 86:
                mid += x.item()
            elif x.item() < 129:
                high += x.item()
            else:
                break
        tempLow.append(low)
        tempMid.append(mid)
        tempHigh.append(high)

    freqArray.setdefault("lowArray", tempLow)
    freqArray.setdefault("midArray", tempMid)
    freqArray.setdefault("highArray", tempHigh)
    for key in list(freqArray.keys()):
        freqArray[str(key) + "_avg"] = max(freqArray[key])

    variance = 1

    start = time()
    end = time()
    while (end - start) < 6000:
        for num in range(bufferSize):
            fftx, fft, freqBins, freqAmp = ear.get_audio_features()
            for i, x in enumerate(freqBins):
                # if x.item() < 129:
                #     freqArray[x.item()][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                if 20 < x.item() < 43:
                    freqArray["lowArray"][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                elif x.item() < 86:
                    freqArray["midArray"][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                elif x.item() < 129:
                    freqArray["highArray"][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                    break

            for key in list(freqArray.keys()):
                if "_avg" not in str(key):
                    beat_limit = freqArray[str(key) + "_avg"] + (freqArray[str(key) + "_avg"] * variance)
                    freq = freqArray[key][num]
                    if freq > beat_limit:
                        print(key)
                        beat(ip, packet)
                        packet = "turn_to_half" if packet == "turn_to_full" else "turn_to_full"
                        break

            for key in list(freqArray.keys()):
                if "_avg" not in str(key):
                    freqArray[str(key) + "_avg"] = (sum(freqArray[key])) / len(freqArray[key])
                    for x in freqArray[key]:
                        variance += (
                            freqArray[key + "_avg"] / x
                            if freqArray[key + "_avg"] / x > 1
                            else x / freqArray[key + "_avg"]
                        )
                    variance = variance / len(freqArray[key])

            variance = variance * 4
            end = time()


if __name__ == "__main__":
    main()
