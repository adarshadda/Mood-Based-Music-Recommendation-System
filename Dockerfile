FROM python:3.8.10-slim

COPY requirements.txt requirements.txt
COPY app app

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt install software-properties-common -y \
    && apt-get install build-essential -y \
    && python3 --version \
    && pip3 install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

WORKDIR app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["python3", "server.py"]
