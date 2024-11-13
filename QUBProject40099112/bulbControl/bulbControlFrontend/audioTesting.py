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
                    device = 10,                    # Pyaudio (portaudio) device index, defaults to first mic input
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
midArray = []
highArray = []
lowAvg = 1
midAvg = 1
highAvg = 1


for x in range(bufferSize):
    fftx, fft, freqBins, freqAmp = ear.get_audio_features()
    lowFreq = 1
    midFreq = 1
    highFreq = 1
    for i, x in enumerate(freqBins):
        if x < 43:
            lowFreq += freqAmp[i].item()
        elif 43 < x < 86:
            midFreq += freqAmp[i].item()
        elif 86 < x < 129:
            highFreq += freqAmp[i].item()
        else:
            break
    lowArray.append(lowFreq)
    midArray.append(midFreq)
    highArray.append(highFreq)


brightness = 100
sensitivity = 2

start = time()
end = time()
while (end - start) < 600:
    for num in range(bufferSize):
        fftx, fft, freqBins, freqAmp = ear.get_audio_features()

        lowFreq = 0
        midFreq = 0
        highFreq = 0
        for i, x in enumerate(freqBins):
            
            if x.item() < 129:
                freqArray[x]
            else:
                break

        if ((lowFreq >= (lowAvg + abs(lowAvg/sensitivity))) and (midFreq >= (midAvg + 
                abs(midAvg/sensitivity))) and (highFreq >= (highAvg + 
                abs(highAvg/sensitivity)))) and not lowAvg <= 1 and not midAvg <= 1 and not highAvg <= 1:
            if brightness < 50:
                brightness = 100
                beat(brightness)
            else:
                brightness = 10
                beat(brightness)
        lowArray[num] = lowFreq
        midArray[num] = midFreq
        highArray[num] = highFreq
        
        lowAvg = _sum(lowArray)/len(lowArray)
        lowVar = 0
        for x in lowArray:
            lowVar += (x - lowAvg)**2
        lowVar = lowVar/len(lowArray)
        midAvg = _sum(midArray)/len(midArray)
        highAvg = _sum(highArray)/len(highArray)

        end = time()
