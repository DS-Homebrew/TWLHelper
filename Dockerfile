FROM python:3.11-slim-bookworm

ENV HOME /home/twlhelper
RUN useradd -m twlhelper
WORKDIR $HOME
COPY ./requirements.txt .
RUN apt-get update \
    && apt-get -y install ffmpeg gifsicle wget \
    && pip install --no-compile --no-cache-dir -r requirements.txt \
    && wget https://github.com/lifehackerhansol/grit/releases/download/v0.9.2/grit \
    && mv grit /usr/local/bin \
    && chmod 0755 /usr/local/bin/grit
USER twlhelper

COPY twlhelper.py twlhelper.py
COPY settings.py settings.py
COPY utils utils
COPY cogs cogs

RUN ln -sf /run/secrets/twlhelper-settings settings.json

CMD ["python3", "twlhelper.py"]
