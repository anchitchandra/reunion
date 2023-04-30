FROM python:3.8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000
# Run Django migrations, collectstatic, and start the server
CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --no-input && \
    python manage.py runserver 0.0.0.0:8000