import argparse
import sys
import os
import pyttsx3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.logging.output as log_output

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('-t', '--text', type=str, required=True, help='Text to read')
parser.add_argument('-v', '--verbose', type=bool, default=False, help='Verbose mode')

args = parser.parse_args()
verbose = args.verbose
text = args.text

class TTS():
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume',1.0)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)

        log_output.output("TTS initialized", verbose=verbose)


    def speak(self, text: str, verbose: bool = False) -> None:
        log_output.output("Speaking...", verbose=verbose)
        log_output.output(f"Text: {text}", verbose=verbose)
        self.engine.say(text)
        self.engine.runAndWait()
        log_output.output("Finished speaking.", verbose=verbose)
        
def main():
    tts = TTS()
    tts.speak(text, verbose=verbose)

if __name__ == '__main__':
    main()