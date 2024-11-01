import time
import yaml

import output as log
import simpleaudio as sa

import base.base as base
import input.packer as packer
import out.tts as tts

python_path = r"./.venv/Scripts/python.exe"

def main():
    
    with open("settings\config.yml", "r") as file:
        config = yaml.safe_load(file)
        wakeWord = config.get('WakeWord', False)
        textResponseModel = config.get('TextResponseModel', "mistral")
        RAGEmbeddingModel = config.get('RAGEmbeddingModel', "mistral")
        verbose = config.get('Verbose', False)
        speechToText = config.get('SpeechToText', True)
        STTModelPath = config.get('STTModelPath', "")
        textToSpeech = config.get('TextToSpeech', True)
        testing =  config.get('Testing', False)
        
    
    log.title("FRIDAY", verbose=verbose)
    log.output("Starting FRIDAY", output_type=log.OutputType.DEBUG, verbose=verbose)
    if verbose:
        for _ in log.track(range(10), description=log.track_desc_gen("Initializing...")):
            time.sleep(0.05)
            
    friday = base.Friday(textResponseModel=textResponseModel, RAGEmbeddingModel=RAGEmbeddingModel, verbose=verbose, testing=testing)
    if textToSpeech: speaker = tts.TTS(verbose=verbose)
    
    while True:
        if wakeWord:
            while True:
                wakeWordSwitch = False
                log.output("Listening for wake word...", output_type=log.OutputType.DEBUG, verbose=verbose)
                packet: packer.Packet = packer.Packet(verbose=verbose, speechToText=speechToText).new(STTModelPath=STTModelPath)
                prompt = packet.text
                if prompt.lower() == "friday":
                    wakeWordSwitch = True
                    try:
                        wave_obj = sa.WaveObject.from_wave_file("D:\\Current\\FRIDAY\\src\\main\\active-beep.wav")
                        wave_obj.play()
                    except FileNotFoundError:
                        log.output("Audio file not found. Please ensure the file exists to use wake word functionality", output_type=log.OutputType.WARNING, verbose=verbose)
                    except ImportError:
                        log.output("simpleaudio module not found. Please install simpleaudio to use wake word functionality", output_type=log.OutputType.WARNING, verbose=verbose)
                    break
                elif "exit" in prompt.lower():
                    log.output("Exiting...", output_type=log.OutputType.DEBUG, verbose=verbose)
                    exit()
                else:
                    log.output("No wake word detected", output_type=log.OutputType.DEBUG, verbose=verbose)
        
        while True if not wakeWord else wakeWordSwitch:
            if wakeWord: wakeWordSwitch = False
            packet: packer.Packet = packer.Packet(verbose=verbose, speechToText=speechToText).new(STTModelPath=STTModelPath)
            prompt = packet.text
            
            if "exit" in prompt.lower():
                log.output("Exiting...", output_type=log.OutputType.DEBUG, verbose=verbose)
                exit()
                
            log.output("Prompting FRIDAY", output_type=log.OutputType.DEBUG, verbose=verbose)
            packet = packer.Packet(text=prompt, emotion="", verbose=verbose)
            if packet.verify():
                output = friday.prompt(packet=packet, verbose=verbose)
            else:
                log.output("Empty packet", output_type=log.OutputType.WARNING, verbose=verbose)
                continue
            
            if textToSpeech:
                log.output("Starting TextToSpeech", output_type=log.OutputType.DEBUG, verbose=verbose)
                speaker.speak(output)
            else:
                log.output(f"[red]Friday >> {output}[/]", verbose=True) 


if __name__ == "__main__":
    main()