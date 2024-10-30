from vosk import Model, KaldiRecognizer
import sounddevice as sd
import sys
import queue
import json

q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

model = Model(r"./src/input/models/vosk-model-small-en-us-0.15")

samplerate = 16000
blocksize = 8192
device = None # Default input device

try:
    device_info = sd.query_devices(sd.default.device, "input") if device is None else device
    
    with sd.RawInputStream(samplerate=samplerate, blocksize=blocksize, device=device,
            dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, samplerate)

        final_text = None
        while final_text == None:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_dict = json.loads(result)
                final_text = result_dict['text']
                
                print(final_text)
            else:
                partial_result = rec.PartialResult()

except KeyboardInterrupt:
    exit()
    
except Exception as e:
    print(e)
    