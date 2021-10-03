# syntax=docker/dockerfile:1

FROM python:3.9.4-alpine AS basepociag
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /app/
RUN apk add --update --no-cache g++ linux-headers
WORKDIR /app
RUN pip install -r requirements.txt