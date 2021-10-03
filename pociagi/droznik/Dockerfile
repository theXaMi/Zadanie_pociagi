# syntax=docker/dockerfile:1

FROM python:3.9.4-slim-buster AS basedb
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /app/
WORKDIR /app
RUN apt-get update && apt-get install -y procps
RUN pip install -r requirements.txt
CMD [ "python", "./pociagi/droznik/droznik.py" ]