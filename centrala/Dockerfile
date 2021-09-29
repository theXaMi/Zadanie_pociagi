# syntax=docker/dockerfile:1

FROM python:alpine AS basecentrala
EXPOSE 102
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /
RUN pip install -r requirements.txt
CMD [ "python", "centrala/centrala.py" ]