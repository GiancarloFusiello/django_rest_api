FROM python:3.7

ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src