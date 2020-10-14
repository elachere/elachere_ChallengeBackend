FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /groover_challenge

WORKDIR /groover_challenge

ADD . /groover_challenge/

RUN pip install -r requirements.txt
