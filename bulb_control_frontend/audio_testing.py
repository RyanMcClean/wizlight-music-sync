# pylint: disable=E1101, not-callable
"""File for synchronising the audio beat with the music
being played through the specified audio device
"""

__author__ = "Ryan Urquhart"
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


def get_working_device_list():
    """Get a list of all tested and working audio devices on the system"""
    devices = []
    pa = pyaudio.PyAudio()
    device_count = pa.get_device_count()
    for num in range(device_count):
        device = pa.get_device_info_by_index(num)
        if device["index"] is not None and valid_low_rate(pa, device["index"]):
            devices.append(
                {
                    "num": device["index"],
                    "name": device["name"],
                    "maxInputChannels": device["maxInputChannels"],
                }
            )
    pa.terminate()
    return devices


def valid_low_rate(pa, device, test_rates=None, test_rate=None):
    """Set the rate to the lowest supported audio rate."""
    if test_rates is None:
        test_rates = [96000, 48000, 44100, 22050, 11025]
    test_rates.append(test_rate)
    for testrate in test_rates:
        if test_device(pa, device, rate=testrate):
            return True
    return False


def test_device(pa, device: int, rate=None):
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
            except OSError:
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

        except OSError:
            return False

        return True
    except OSError as e:
        print(e)
        import traceback  # pylint: disable=C0415

        traceback.print_exc()
        time.sleep(3)
        return False


try:
    from . import variables
except ImportError:
    import variables


def beat(ip, packet):
    """Send a beat packet to the bulb"""
    variables.message_loud("\nbeat\n")
    variables.client.sender(ip, packet, expected_results=-1)


def main(device=None):
    """Main function to run the audio sync"""
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
        ip = bulb.bulb_ip
        variables.client.sender(ip, "turn_on", attempts=5)

    buffer_size = 100

    freq_array = {}

    temp_low = []
    temp_mid = []
    temp_high = []

    # Get the initial values for the low, mid and high frequencies
    for x in range(buffer_size):
        _, _, freq_bins, freq_amp = ear.get_audio_features()
        low = 0
        mid = 0
        high = 0
        for i, x in enumerate(freq_bins):
            if x.item() < 50:
                low += x.item()
            elif x.item() < 100:
                mid += x.item()
            elif x.item() < 150:
                high += x.item()
            else:
                break
        temp_low.append(low)
        temp_mid.append(mid)
        temp_high.append(high)

    freq_array.setdefault("lowArray", temp_low)
    freq_array.setdefault("midArray", temp_mid)
    freq_array.setdefault("highArray", temp_high)
    for key in list(freq_array.keys()):
        freq_array[str(key) + "_avg"] = max(freq_array[key])

    # Set initial values for variance, this will be changed by the equations later
    variance = 1
    while variables.music_sync:
        for num in range(buffer_size):
            _, _, freq_bins, freq_amp = ear.get_audio_features()
            for i, x in enumerate(freq_bins):
                # the 'else 1' is to prevent division by zero errors
                if x.item() < 50:
                    freq_array["lowArray"][num] = (
                        freq_amp[i].item() if freq_amp[i].item() != 0 else 1
                    )
                elif x.item() < 100:
                    freq_array["midArray"][num] = (
                        freq_amp[i].item() if freq_amp[i].item() != 0 else 1
                    )
                elif x.item() < 150:
                    freq_array["highArray"][num] = (
                        freq_amp[i].item() if freq_amp[i].item() != 0 else 1
                    )
                    break

            for key in list(freq_array.keys()):
                if "_avg" not in str(key):
                    beat_limit = freq_array[str(key) + "_avg"] + (
                        freq_array[str(key) + "_avg"] * variance
                    )
                    freq = freq_array[key][num]
                    if freq > beat_limit:
                        variables.message_loud(key)
                        for bulb in variables.bulbs:
                            ip = bulb.bulb_ip
                            beat_thread = Thread(target=beat, args=(ip, packet))
                            beat_thread.start()
                        packet = "turn_to_half" if packet == "turn_to_full" else "turn_to_full"
                        time.sleep(0.01)
                        break

            for key in list(freq_array.keys()):
                if "_avg" not in str(key):
                    freq_array[str(key) + "_avg"] = (sum(freq_array[key])) / len(freq_array[key])
                    per_diff = 0
                    for x in freq_array[key]:
                        per_diff += freq_array[key + "_avg"] / x
                    if per_diff > 1:
                        variance = per_diff / len(freq_array[key])
                    else:
                        variance = pow(per_diff, -1) / len(freq_array[key])

    ear.stream_reader.terminate()


if __name__ == "__main__":
    if not hasattr(variables, "init"):
        variables.init()
    main()
