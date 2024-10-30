import argparse
import sys
import os
import pyttsx3
import subprocess
import soundfile as sf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.logging.output as log_output

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('-t', '--text', type=str, required=True, help='Text to TTS')
parser.add_argument('-v', '--verbose', type=bool, default=False, help='Verbose mode')

args = parser.parse_args()
verbose = args.verbose
text = args.text

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models', 'en_GB-southern_english_female-low.onnx'))
piper_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'piper', 'piper.exe'))

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
        #log_output.output(f"Text: {text}", verbose=verbose)
        #self.engine.say(text)
        #self.engine.runAndWait()

        # piper --model en_US-lessac-high.onnx --output_file hello.wav < hello.txt
        result = subprocess.run(
            [piper_path, "--model", model_path, "--output_file", "hello.wav"],
            input=text.encode('utf-8'),
            capture_output=True
        )
        data, samplerate = sf.read('hello.wav')
        sf.write('output.wav', data, samplerate)
        subprocess.run(["start", "output.wav"], shell=True)
        log_output.output("Finished speaking.", verbose=verbose)
        
def main():
    tts = TTS()
    tts.speak(text, verbose=verbose)

if __name__ == '__main__':
    main()