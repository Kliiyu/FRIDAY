import subprocess
import os
import sys
import json
import random
from datetime import datetime
from enum import Enum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.logging.output as log_output

venv_python_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.venv/Scripts/python.exe'))
speech_recognition_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'speech_recognition.py'))
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../base/main.py'))

verbose = True
STT = False

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
            timestamp: str = "",
        ):
        self.text: str = text
        self.emotion: str = random.choice(list(Emotion)).value if emotion == "" else emotion
        self.timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if timestamp == "" else timestamp
        log_output.output(f"Packet initialized", verbose=verbose)

    def __str__(self) -> str:
        return json.dumps({
            "text": self.text,
            "emotion": self.emotion,
            "timestamp": self.timestamp
        })
    
    def __sizeof__(self) -> int:
        return len(str(self))
    
    def generate(self) -> 'Packet':
        try:
            if STT:
                output = subprocess.run([venv_python_path, speech_recognition_path], capture_output=True)
                self.text = output.stdout.decode('utf-8').strip()
            else: 
                self.text = log_output.inp("You >> ")

            log_output.output(f"Packet generated", verbose=verbose)
            return self
        except KeyboardInterrupt:
            log_output.output("Exiting...", verbose=verbose, output_type=log_output.OutputType.WARNING)
            exit()

        except FileNotFoundError:
            log_output.outputt("File not found", verbose=verbose, output_type=log_output.OutputType.ERROR)
            exit()

        except Exception as e:
            print(e)

    def verify(self) -> bool:
        return self.text != ""
    
def str_to_packet(packet: str) -> Packet:
    packet = json.loads(packet)
    return Packet(packet["text"], packet["emotion"], packet["timestamp"])


def main():
    while True:
        pckt = Packet().generate()
        if pckt.verify():
            log_output.output(pckt, verbose=verbose)

            try:
                log_output.output("Packet sent", verbose=verbose)
                subprocess.run([venv_python_path, base_path, "--packet", str(pckt), "--verbose", str(verbose)])
                log_output.output("Base finished running", verbose=verbose)

            except FileNotFoundError:

                log_output.output("File not found", verbose=verbose, output_type=log_output.OutputType.ERROR)
                exit()

            except Exception as e:
                log_output.output(e, verbose=verbose, output_type=log_output.OutputType.ERROR)
        else:
            log_output.output("Emtpy packet", verbose=verbose)

if __name__ == "__main__":
    main()
