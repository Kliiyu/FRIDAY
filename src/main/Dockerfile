# Dockerfile

# Use Ubuntu as the base image
FROM ubuntu

# Set the working directory
WORKDIR /home/app

# Copy the application files, including the local Ollama tar file, into the container
COPY . .

# Install Python and related dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv portaudio19-dev curl

# Install Ollama using the local tar file
RUN tar -C /usr -xzf ollama-linux-amd64.tgz

# Pull the 'mistral' model after ensuring Ollama is installed
RUN /usr/bin/ollama serve & \
    sleep 5 && \
    ollama pull mistral

# Set up the Python virtual environment and install dependencies
RUN python3 -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

# Set the default command to run the main application
CMD [".venv/bin/python", "main.py"]
