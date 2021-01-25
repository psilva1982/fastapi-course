FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt / 
RUN python3 -m pip install -r /requirements.txt

# Copy api files do Docker Image
# COPY . /app
# WORKDIR /app

COPY . /app
WORKDIR /app