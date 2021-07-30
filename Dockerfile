FROM python:3.9-slim
LABEL org.opencontainers.image.source https://github.com/DS-Homebrew/TWLHelper
ENV IS_DOCKER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HOME /home/twlhelper
RUN useradd -m -d $HOME -s /bin/sh -u 2849 twlhelper
WORKDIR $HOME
COPY ./requirements.txt .
RUN pip install --no-compile --no-cache-dir -r requirements.txt
USER twlhelper
ARG BRANCH="unknown"
COPY . .
CMD ["python3", "twlhelper.py"]
