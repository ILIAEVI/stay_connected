FROM continuumio/miniconda3
LABEL authors="giorgi"

RUN apt-get update \
    && apt-get install -y libmagic1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/djangoapp/src

WORKDIR /home/djangoapp/src

COPY ./requirements.txt /home/djangoapp/src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/djangoapp/src/

RUN python3 manage.py collectstatic --noinput

RUN python3 manage.py flush

EXPOSE 8000

#CMD ["sh", "-c", "python3 manage.py migrate && gunicorn stay_connected.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
#CMD ["sh", "-c", "python3 manage.py migrate && python manage.py runserver"]