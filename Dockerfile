FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

RUN mkdir /app

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "5000", "src.app:app"]
