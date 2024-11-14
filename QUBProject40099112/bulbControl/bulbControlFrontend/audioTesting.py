from Realtime_PyAudio_FFT.src.stream_analyzer import Stream_Analyzer
from time import sleep, time
from socket import *

def _sum(arr):
    sum = 0
    for i in arr:
        sum += i
    return sum

def beat(brightness):
    print("\nbeat\n")
    sock.sendto(b"{\"id\":1,\"method\":\"setPilot\",\"params\":{\"temp\":2000,\"dimming\":" + bytes(str(brightness), 'utf-8') + b"}}", (ip, port))
    sleep(0.1)

ip = '192.168.50.128'
port = 38899
packet_query = b"{\"method\":\"getPilot\",\"params\":{}}"
packet_on = b"{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":true}}"
packet_half = b"{\"id\":1,\"method\":\"setPilot\",\"params\":{\"temp\":2000,\"dimming\":10}}"
packet_full = b"{\"id\":1,\"method\":\"setPilot\",\"params\":{\"temp\":2000,\"dimming\":100}}"

timeout = 0.5


ear = Stream_Analyzer(
                    device = None,                    # Pyaudio (portaudio) device index, defaults to first mic input
                    rate   = None,                 # Audio samplerate, None uses the default source settings
                    FFT_window_size_ms  = 60,       # Window size used for the FFT transform
                    updates_per_second  = 500,      # How often to read the audio stream for new data
                    smoothing_length_ms = 50,       # Apply some temporal smoothing to reduce noisy features
                    n_frequency_bins = 150,          # The FFT features are grouped in bins
                    visualize = False,
                    verbose = True 
                    )

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('', port))
sock.sendto(b"{\"id\":1,\"method\":\"setPilot\",\"params\":{\"temp\":2000,\"dimming\":100}}", (ip, port))

bufferSize = 100

freqArray = {}


for x in range(bufferSize):
    fftx, fft, freqBins, freqAmp = ear.get_audio_features()
    for i, x in enumerate(freqBins):
        if x.item() < 129:
            freqArray.setdefault(x.item(), []).append(freqAmp[i].item())
        else:
            break
for x in range(len(freqArray.keys())):
    freqArray[x] = _sum(freqArray.keys()[x]) / len(freqArray.keys()[x])


brightness = 100
sensitivity = 2

start = time()
end = time()
while (end - start) < 600:
    for num in range(bufferSize):
        fftx, fft, freqBins, freqAmp = ear.get_audio_features()
        for i, x in enumerate(freqBins):
            if x.item() < 129:
                freqArray[x.item()][num] = freqAmp[i].item()
            else:
                break

        for x in freqArray.keys():
            if '_avg' not in x and freqArray[x][num] >= freqArray[str(x) + "_avg"] + (freqArray[str(x) + "_avg"] / sensitivity):
                beat(brightness)
                if brightness > 50:
                    brightness = 10
                else:
                    brightness = 100
        
        for x in freqArray.keys():
            if '_avg' not in x:
                freqArray[str(x) + "_avg"] = _sum(freqArray[x]) / len(freqArray[x])
        end = time()
