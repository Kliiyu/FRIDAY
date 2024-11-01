# Dockerfile

FROM ubuntu
WORKDIR /home/app

COPY . .

# Install Python and related dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# Create and activate virtual environment, then install requirements
RUN python3 -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

CMD [".venv/bin/python", "main.py"]
