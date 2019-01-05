FROM ubuntu
MAINTAINER loblab

ARG APT_MIRROR=mirrors.163.com
ARG PYTHON=python3

RUN sed -i "s/archive.ubuntu.com/$APT_MIRROR/" /etc/apt/sources.list
RUN apt-get update --fix-missing && apt-get -y upgrade
RUN apt-get -y install ${PYTHON}-pip
RUN $PYTHON -m pip install --upgrade pip

RUN $PYTHON -m pip install influxdb

