# Record mp3 python
import sounddevice as sd
from scipy.io.wavfile import write

class RecordMe:
    @staticmethod
    def RecordMessage(duration=30):
        fs = 44100  # Sample rate


        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('message.wav', fs, myrecording)  # Save as WAV file 
        pass
    pass