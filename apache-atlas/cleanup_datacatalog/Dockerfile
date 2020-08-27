# docker build -t rdbms-datacatalog-cleaner .
FROM python:3.7

ENV GOOGLE_APPLICATION_CREDENTIALS=/data/apache-atlas2dc-credentials.json

WORKDIR /lib
RUN pip install google-cloud-datacatalog

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

ENTRYPOINT ["python", "cleanup_datacatalog.py"]
