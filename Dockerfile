# Download base image ubuntu 18.04
FROM ubuntu:20.04

# LABEL about the custom image
LABEL maintainer="sur5an@yahoo.com"
LABEL version="0.1"
LABEL description="This is custom Docker Image for \
my test raspberry pi project."

# Install updates to base image
RUN \
  apt-get update -y \
  && apt-get install -y

RUN \
    apt-get install vim -y

RUN \
    apt-get install python3 -y \
    && apt-get install python3-pip -y

RUN \
    pip3 install slackclient

RUN mkdir -p /var/slack/
COPY slack/*.py  /var/slack/

CMD ["python3","/var/slack/listen.py"]