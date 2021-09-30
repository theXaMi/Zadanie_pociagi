# syntax=docker/dockerfile:1

FROM python:alpine AS basecentrala
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
EXPOSE 1200
COPY . /app/
WORKDIR /app
RUN ls | tr -s '\n' ' ' && sleep 10
RUN pip install -r requirements.txt
CMD [ "python", "centrala.py" ]