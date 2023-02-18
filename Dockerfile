FROM python:3.8-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip

COPY requirements.txt .

COPY dump.json .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY news/ .

CMD ["gunicorn", "news.wsgi:application", "--bind", "0:8000"]