"""File for synchronising the audio beat with the music
being played through the specified audio device
"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

try:
    import pyaudiowpatch as pyaudio
except ImportError:
    import pyaudio

from threading import Thread
import time

try:
    from .Realtime_PyAudio_FFT.stream_analyzer import Stream_Analyzer

except ImportError:
    from Realtime_PyAudio_FFT.stream_analyzer import Stream_Analyzer


def getWorkingDeviceList():
    devices = []
    pa = pyaudio.PyAudio()
    device_count = pa.get_device_count()
    for num in range(device_count):
        device = pa.get_device_info_by_index(num)
        if valid_low_rate(pa, device["index"]):
            devices.append(
                {"num": device["index"], "name": device["name"], "maxInputChannels": device["maxInputChannels"]}
            )
    pa.terminate()
    return devices

def valid_low_rate(pa, device, test_rates=[96000, 48000, 44100, 22050, 11025], test_rate=None):
        """Set the rate to the lowest supported audio rate."""
        test_rates.append(test_rate)
        for testrate in test_rates:
            if test_device(pa, device, rate=testrate):
                return True
        return False

def test_device(pa, device, rate=None):
        """given a device ID and a rate, return True/False if it's valid."""
        try:
            info = pa.get_device_info_by_index(device)

            if not info["maxInputChannels"] > 0:
                return False

            try:
                try:
                    stream = pa.open(
                        format=pyaudio.paInt16,
                        channels=1,
                        input_device_index=device,
                        frames_per_buffer=1024,
                        rate=rate,
                        input=True,
                    )
                    time.sleep(1)
                    stream.stop_stream()
                    stream.close()
                except:
                    stream = pa.open(
                        format=pyaudio.paInt8,
                        channels=2,
                        input_device_index=device,
                        frames_per_buffer=1024,
                        rate=rate,
                        input=True,
                    )
                    time.sleep(1)
                    stream.stop_stream()
                    stream.close()

            except Exception as err:
                # print(err)
                return False

            return True
        except Exception as e:
            print("\n\n\n\n")
            print(e)
            import traceback

            traceback.print_exc()
            time.sleep(3)
            print("\n\n\n\n")
            return False


try:
    from . import variables
except ImportError:
    import variables


def beat(ip, packet):
    variables.messageLoud("\nbeat\n")
    variables.client.sender(ip, packet, expected_results=-1)


def main(device=None):
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
    for bulb in variables.bulbs:
        ip = bulb.bulbIp
        variables.client.sender(ip, "turn_on", attempts=5)

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
            if x.item() < 50:
                low += x.item()
            elif x.item() < 100:
                mid += x.item()
            elif x.item() < 150:
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
    while variables.musicSync:
        for num in range(bufferSize):
            fftx, fft, freqBins, freqAmp = ear.get_audio_features()
            for i, x in enumerate(freqBins):
                if x.item() < 50:
                    freqArray["lowArray"][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                elif x.item() < 100:
                    freqArray["midArray"][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                elif x.item() < 150:
                    freqArray["highArray"][num] = freqAmp[i].item() if freqAmp[i].item() != 0 else 1
                    break

            for key in list(freqArray.keys()):
                if "_avg" not in str(key):
                    beat_limit = freqArray[str(key) + "_avg"] + (freqArray[str(key) + "_avg"] * variance)
                    freq = freqArray[key][num]
                    if freq > beat_limit:
                        variables.messageLoud(key)
                        for bulb in variables.bulbs:
                            ip = bulb.bulbIp
                            beat_thread = Thread(target=beat, args=(ip, packet))
                            beat_thread.start()
                        packet = "turn_to_half" if packet == "turn_to_full" else "turn_to_full"
                        time.sleep(0.01)
                        break

            for key in list(freqArray.keys()):
                if "_avg" not in str(key):
                    freqArray[str(key) + "_avg"] = (sum(freqArray[key])) / len(freqArray[key])
                    per_diff = 0
                    for x in freqArray[key]:
                        per_diff += freqArray[key + "_avg"] / x
                    if per_diff > 1:
                        variance = per_diff / len(freqArray[key])
                    else:
                        variance = pow(per_diff, -1) / len(freqArray[key])

    ear.stream_reader.terminate()


if __name__ == "__main__":
    if not hasattr(variables, "init"):
        variables.init()
    main()
