import json
import random
from datetime import datetime
from enum import Enum

import output as log
import input.speech_to_text as sr

python_path = r"../.venv/Scripts/python.exe"

class Emotion(Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    NEUTRAL = "neutral"

class Packet:
    def __init__(
            self, 
            text: str = "",
            emotion: str = "",
            **kwargs
        ):
        try:
            self.text: str = text
            self.emotion: str = random.choice(list(Emotion)).value if emotion == "" else emotion
            self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.verbose: bool = kwargs.get('verbose', False)
            self.speechToText: bool = kwargs.get('speechToText', True)
            
            log.output(f"Packet initialized", verbose=self.verbose)
        except Exception as e:
            log.output(f"Exception in packer.py @ Packet.__init__(); {e}", verbose=self.verbose, output_type=log.OutputType.ERROR)

    def __str__(self) -> str:
        return json.dumps({
            "text": self.text,
            "emotion": self.emotion,
            "timestamp": self.timestamp
        })
    
    def __sizeof__(self) -> int:
        return len(str(self))
    
    def new(self, **kwargs) -> 'Packet':
        try:
            if self.speechToText:
                log.output("Listening...", verbose=self.verbose)
                
                recognizer = sr.Recognizer(model=kwargs.get('STTModelPath', ""))
                self.text = recognizer.listen()
                log.output(f"[red]Heard: {self.text}[/]", verbose=self.verbose)
            else: 
                log.output("Listening disabled", verbose=self.verbose)
                self.text = log.inp("You >> ")

            log.output(f"Packet generated", verbose=self.verbose)
            return Packet(self.text, self.emotion, verbose=self.verbose)
        except KeyboardInterrupt:
            log.output("Exiting...", verbose=self.verbose, output_type=log.OutputType.WARNING)
            exit()

        except FileNotFoundError:
            log.outputt("File not found", verbose=self.verbose, output_type=log.OutputType.ERROR)
            exit()

        except Exception as e:
            log.output(f"Exception in packer.py @ Packet.new(); {e}", verbose=self.verbose, output_type=log.OutputType.ERROR)

    def verify(self) -> bool:
        return self.text != ""
    
def str_to_packet(packet: str) -> Packet:
    packet = json.loads(packet)
    return Packet(packet["text"], packet["emotion"], packet["timestamp"])
