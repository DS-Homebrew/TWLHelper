FROM python:3.9-slim
LABEL org.opencontainers.image.source https://github.com/DS-Homebrew/DSi-Hacking-Bot
ENV IS_DOCKER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HOME /home/twlbot
RUN useradd -m -d $HOME -s /bin/sh -u 2849 twlbot
WORKDIR $HOME
COPY ./requirements.txt .
RUN pip install --no-compile --no-cache-dir -r requirements.txt
USER twlbot
ARG BRANCH="unknown"
COPY . .
CMD ["python3", "twlbot.py"]
