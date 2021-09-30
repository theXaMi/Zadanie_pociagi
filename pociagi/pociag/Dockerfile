# syntax=docker/dockerfile:1

FROM python:alpine AS basepociag
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "pociag.py" ]