FROM python:3.7.15-alpine

COPY /web /web
COPY application.py /application.py
COPY requirements.txt /requirements.txt
COPY /tests /tests

RUN apk add build-base linux-headers
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 5000

CMD flask run
