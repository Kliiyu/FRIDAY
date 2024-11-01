import subprocess
import ollama
import requests
import webbrowser
from langchain_community.document_loaders import WebBaseLoader

import output as log
from memory.retriver import Retriever
from input.packer import Packet

python_path = r"../.venv/Scripts/python.exe"

class Friday():
    def __init__(self, **kwargs):
        self.verbose: bool = kwargs.get('verbose', False)
        self.testing: bool = kwargs.get('testing', False)
        self.textResponseModel: str = kwargs.get('textResponseModel', "mistral")
        self.RAGEmbeddingModel: str = kwargs.get('RAGEmbeddingModel', "mistral")
        log.output("Friday initialized", verbose=self.verbose)

        if self.testing == False:
            loader = WebBaseLoader(
                web_paths=("https://en.wikipedia.org/wiki/Europa_Clipper",),
            )
            docs = loader.load()

            self.tucker = Retriever(self.RAGEmbeddingModel)
            splits = self.tucker.chew(docs)
            self.tucker.hide(splits)


    def prompt(self, packet: Packet, verbose: bool = False) -> str:
        log.output("Prompting FRIDAY", verbose=self.verbose)

        if packet.text in ["nuke", "nook", "anuc", "anuc7777"]:
            webbrowser.open("https://www.youtube.com/watch?v=tQhs5pAhsOg")
        if "girl" in packet.text:
            response = requests.get('https://api.waifu.pics/nsfw/waifu')
            if response.status_code == 200:
                data = response.json()
                webbrowser.open(data["url"])
            else:
                print('Request failed with status code:', response.status_code)

        if self.testing == False:
            question = packet.text
            context = self.tucker.fetch(question)

            formatted_prompt = f"Question: {question}\n\nContext: {context}"
            response = ollama.chat(model=self.textResponseModel, messages=[{"role": "user", "content": formatted_prompt}])
            output = response['message']['content']
        else:
            output = packet.text

        return output
