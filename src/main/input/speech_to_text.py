from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json
import os

import output as log

class Recognizer():
    def __init__(self, **kwargs) -> None:
        try:
            self.q = queue.Queue()
            self.samplerate = 16000
            self.blocksize = 8192
            self.device: int | None = kwargs.get('device', None)
            
            model: str = kwargs.get('model', "")
            if model == "":
                log.output(f"Model not provided in config.yml; speech_to_text.py @ Recognizer.__init__()", output_type=log.OutputType.ERROR)
                return
            if os.path.exists(model) == False:
                log.output(f"Model not found at {model}; speech_to_text.py @ Recognizer.__init__()", output_type=log.OutputType.ERROR)
                return
            self.model = Model(model)
        except Exception as e:
            log.output(f"Exception in speech_to_text.py @ Recognizer.__init__(); {e}", output_type=log.OutputType.ERROR)
        
    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            log.output(status, output_type=log.OutputType.ERROR)
        self.q.put(bytes(indata))
        
    def listen(self):
        try:
            device_info = sd.query_devices(sd.default.device, "input") if self.device is None else self.device
            
            with sd.RawInputStream(samplerate=self.samplerate, blocksize=self.blocksize, device=self.device,
                    dtype="int16", channels=1, callback=self.callback):

                rec = KaldiRecognizer(self.model, self.samplerate)

                final_text = None
                while final_text == None:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = rec.Result()
                        result_dict = json.loads(result)
                        final_text = result_dict['text']
                        
                        return final_text
        except KeyboardInterrupt:
            log.output("Exiting...", output_type=log.OutputType.WARNING)            
        
        except Exception as e:
            log.output(f"Exception in speech_to_text.py @ Recognizer.listen(); {e}", output_type=log.OutputType.ERROR)
    