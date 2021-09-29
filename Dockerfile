# syntax=docker/dockerfile:1

FROM python:alpine AS basedb
EXPOSE 666
LABEL maintainer="XaMi <xamioriginal@gmail.com>"
COPY . /
RUN pip install -r requirements.txt
CMD [ "python", "db/db.py" ]