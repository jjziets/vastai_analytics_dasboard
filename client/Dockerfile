FROM nvidia/cuda:11.6.2-devel-ubuntu20.04

MAINTAINER jjiets

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
  build-essential \
  software-properties-common \
  wget

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update && apt install -y python3.8 python3.8-distutils python3.8-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.8 get-pip.py

WORKDIR /var/lib/vastai_analytics

ADD ./requirements.txt /var/lib/vastai_analytics

RUN python3.8 -m pip install -r requirements.txt

RUN apt install -y apt-transport-https ca-certificates
RUN apt install -y curl 
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get install -y docker-ce
RUN add-apt-repository universe && apt-get update && apt-get install jq -y

ADD . /var/lib/vastai_analytics

ENTRYPOINT /bin/bash /var/lib/vastai_analytics/run.sh
