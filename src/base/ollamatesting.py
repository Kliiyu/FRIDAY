import ollama

stream = ollama.chat(
    model="mistral",
    messages=[{"role": "user", "content": "What is the Europa Clipper?"}],
    stream=True,
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
    
#print(ollama.embeddings(model='mistral', prompt='They sky is blue because of rayleigh scattering'))