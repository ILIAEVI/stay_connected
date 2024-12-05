FROM continuumio/miniconda3
LABEL authors="giorgi"

RUN apt-get update \
    && apt-get install -y libmagic1 && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/services/djangoapp/src

WORKDIR /opt/services/djangoapp/src

COPY ./requirements.txt /opt/services/djangoapp/src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/services/djangoapp/src/

EXPOSE 8000