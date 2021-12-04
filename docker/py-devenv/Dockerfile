FROM ubuntu:latest

RUN apt-get update && apt-get install -y git

FROM python:3.10

#FROM pypi/llvmlite:latest

#FROM tensorflow/tensorflow:latest

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt