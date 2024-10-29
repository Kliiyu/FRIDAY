from vosk import Model, KaldiRecognizer
import PyAudio

MODEL = Model(r"./models/vosk-model-small-en-us-0.15/") 
RECOGNIZER = KaldiRecognizer(MODEL, 16000)

CAP = PyAudio.PyAudio()
STREAM = CAP.open(format=PyAudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
STREAM.start_stream()

while True:
    data = STREAM.read(4096)
    if len(data) == 0:
        break

    if RECOGNIZER.AcceptWaveform(data):
        print(RECOGNIZER.Result())
    else:
        print(RECOGNIZER.PartialResult())