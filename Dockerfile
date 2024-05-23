FROM python:3.11-bookworm

ENV HOME /home/twlhelper
RUN useradd -m twlhelper
WORKDIR $HOME
COPY ./requirements.txt .
RUN apt-get update \
    && apt-get -y install ffmpeg gifsicle curl \
    && pip install --no-compile --no-cache-dir -r requirements.txt

RUN curl -LO https://github.com/lifehackerhansol/grit/releases/download/v0.9.2/grit && mv grit grit-amd64
RUN curl -LO https://github.com/lifehackerhansol/blocksds-grit/releases/download/v1.1.0-blocks/grit && mv grit grit-aarch64
# assume AMD64
RUN if [[ $TARGETPLATFORM = "linux/arm64" ]] ; then mv grit-aarch64 /usr/local/bin/grit ; else mv grit-amd64 /usr/local/bin/grit; fi \
    && chmod 0755 /usr/local/bin/grit
USER twlhelper

COPY twlhelper.py twlhelper.py
COPY settings.py settings.py
COPY utils utils
COPY cogs cogs

RUN ln -sf /run/secrets/twlhelper-settings settings.json

CMD ["python3", "twlhelper.py"]
