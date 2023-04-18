FROM python:3.11-bullseye

ENV HOME /home/twlhelper
RUN useradd -m twlhelper
WORKDIR $HOME
COPY ./requirements.txt .
COPY ./assets/dkp-pacman.sh .
RUN ln -s /proc/mounts /etc/mtab \
    && chmod +x dkp-pacman.sh \
    && apt-get update \
    && ./dkp-pacman.sh \
    && dkp-pacman -Syu --noconfirm \
    && dkp-pacman -S --noconfirm devkit-env grit \
    && apt-get -y install ffmpeg gifsicle \
    && pip install --no-compile --no-cache-dir -r requirements.txt
USER twlhelper

COPY twlhelper.py twlhelper.py
COPY settings.py settings.py
COPY utils utils
COPY cogs cogs

RUN ln -sf /run/secrets/twlhelper-settings settings.json
ENV PATH "/opt/devkitpro/tools/bin:$PATH"

CMD ["python3", "twlhelper.py"]
