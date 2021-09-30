# syntax=docker/dockerfile:1

FROM python:alpine AS basedb
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /app/
RUN apk add g++ linux-headers
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "droznik.py" ]