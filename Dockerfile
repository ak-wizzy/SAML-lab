FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY app/ .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info"]
