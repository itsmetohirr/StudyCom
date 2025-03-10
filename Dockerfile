# Dockerfile
FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "root.wsgi:application"]
