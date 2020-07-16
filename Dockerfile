FROM ubuntu:18.04

RUN apt-get update && \
	apt-get install -y build-essential \
	python3 \
	python3-dev \
	python3-pip 

RUN mkdir /code
WORKDIR /code

COPY . /code/

RUN pip3 install -r requirements.txt

