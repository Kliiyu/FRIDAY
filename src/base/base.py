import argparse
import sys
import os
import yaml
import subprocess
import ollama
import requests
import webbrowser
from langchain_community.document_loaders import WebBaseLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.logging.output as log_output
import settings.prompts.default as default_prompts
from src.input.packer import Packet, str_to_packet, venv_python_path
from src.memory.retriver import Retriever

output_tts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../output/tts.py'))

parser = argparse.ArgumentParser(description='Process some arguments.')
parser.add_argument('-p', '--packet', type=str, required=True, help='Packet JSON')
parser.add_argument('-v', '--verbose', type=bool, default=False, help='Verbose mode')

args = parser.parse_args()
verbose = args.verbose
pckt = str_to_packet(args.packet)

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../settings/config.yml')), 'r') as config_file:
    config = yaml.safe_load(config_file)
    TTS = config.get('TextToSpeech', False)
    TextResponseModel = config.get('TextResponseModel', "mistral")
    NoAITesting = config.get('NoAITesting', False)

class Friday():
    def __init__(self):
        log_output.output("Friday initialized", verbose=verbose)

        if NoAITesting == False:
            loader = WebBaseLoader(
                web_paths=("https://en.wikipedia.org/wiki/Europa_Clipper",),
            )
            docs = loader.load()

            self.tucker = Retriever()
            splits = self.tucker.chew(docs)
            self.tucker.hide(splits)


    def prompt(self, packet: Packet, verbose: bool = False) -> str:
        log_output.output("Prompting FRIDAY", verbose=verbose)

        if packet.text in ["nuke", "nook", "anuc", "anuc7777"]:
            webbrowser.open("https://www.youtube.com/watch?v=tQhs5pAhsOg")
        if "girl" in packet.text:
            response = requests.get('https://api.waifu.pics/nsfw/waifu')
            if response.status_code == 200:
                data = response.json()
                webbrowser.open(data["url"])
            else:
                print('Request failed with status code:', response.status_code)

        if NoAITesting == False:
            question = packet.text
            context = self.tucker.fetch(question)

            formatted_prompt = f"Question: {question}\n\nContext: {context}"
            response = ollama.chat(model=TextResponseModel, messages=[{"role": "user", "content": formatted_prompt}])
            output = response['message']['content']
        else:
            output = packet.text

        if TTS:
            self.speak(output, verbose=verbose)
        else:
            log_output.output(f"Friday >> {output}", verbose=verbose)
    
    def speak(self, text: str, verbose: bool = False) -> None:
        subprocess.run([venv_python_path, output_tts_path, "--text", str(text), "--verbose", str(verbose)])


def main():
    friday = Friday()
    friday.prompt(pckt, verbose=verbose)


if __name__ == '__main__':
    main()