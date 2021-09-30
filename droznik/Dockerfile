# syntax=docker/dockerfile:1

FROM python:alpine AS basedroznik
EXPOSE 102
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /
RUN apk add libc-dev g++ linux-headers
RUN pip install -r requirements.txt
CMD [ "python", "droznik/droznik.py" ]