FROM python:3.8.10-slim

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt install software-properties-common -y \
    && apt-get install build-essential -y \
    && python3 --version \
    && apt update \
    && apt install ffmpeg -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt update \
    && apt install nginx -y

### Set up user with permissions
# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

### Set up app-specific content
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user app $HOME/app

### Update permissions for the app
USER root
RUN chmod 755 ~/app/*
USER user

# RUN python3 server.py
ENTRYPOINT ["python3", "app.py"]
# ENTRYPOINT ["gunicorn", "--timeout 600", "wsgi:app"]
