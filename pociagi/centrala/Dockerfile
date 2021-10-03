# syntax=docker/dockerfile:1

FROM python:3.9.5-slim-buster AS basecentrala
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
EXPOSE 1200
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt