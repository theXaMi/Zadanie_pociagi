# syntax=docker/dockerfile:1

FROM python:alpine AS basecentrala
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
EXPOSE 1200
COPY . /app/
RUN apk add g++ linux-headers
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "centrala.py" ]