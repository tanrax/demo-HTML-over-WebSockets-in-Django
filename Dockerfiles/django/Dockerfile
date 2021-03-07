FROM debian:stable-slim

ENV PYTHONUNBUFFERED: 1

# set work directory
WORKDIR /usr/src/app

# install software
RUN apt update
RUN apt install -y build-essential cron python3-pip gettext

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# launcher
COPY django-launcher.dev.sh /django-launcher.dev.sh
COPY django-launcher.pro.sh /django-launcher.pro.sh
RUN chmod +x /django-launcher.dev.sh
RUN chmod +x /django-launcher.pro.sh
