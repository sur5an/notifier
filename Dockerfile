# Download base image ubuntu 18.04
FROM ubuntu:20.04
ARG MARIADB_PASS
ENV MARIADB_PASS=$var_name
# LABEL about the custom image
LABEL maintainer="sur5an@yahoo.com"
LABEL version="0.1"
LABEL description="This is custom Docker Image for \
my test raspberry pi project."

# Install updates to base image
RUN \
  apt-get update -y \
  && apt-get install -y \
  && apt update -y \
  && apt -y upgrade

RUN \
    apt-get install vim -y

RUN \
    apt-get install python3 -y \
    && apt-get install python3-pip -y

RUN \
    pip3 install slackclient

#RUN \
#    apt install software-properties-common -y

RUN \
    export DEBIAN_FRONTEND=noninteractive \
    && rm -f /tmp/m \
    && echo 'mariadb-server-10.0 mysql-server/root_password password $MARIADB_PASS' >> /tmp/m \
    && echo 'mariadb-server-10.0 mysql-server/root_password_again password $MARIADB_PASS' >> /tmp/m \
    && debconf-set-selections /tmp/m \
    && apt-get install mariadb-server mariadb-client -y \
    && /etc/init.d/mysql restart


RUN mkdir -p /var/slack/
COPY slack/*.py  /var/slack/

CMD ["python3","/var/slack/listen.py"]