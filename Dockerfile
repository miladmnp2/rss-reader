FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
VOLUME /app

COPY /codes/requirements.txt .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt
