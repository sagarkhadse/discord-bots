FROM python:3.8-alpine

WORKDIR /bots
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .