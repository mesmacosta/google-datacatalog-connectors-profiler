# docker build -t rdbms-datacatalog-cleaner .
FROM python:3.7

ENV GOOGLE_APPLICATION_CREDENTIALS=/data/hive2dc-credentials.json

WORKDIR /lib
COPY ./lib/datacatalog-python.tar.gz .
RUN tar -xvf ./datacatalog-python.tar.gz
RUN pip install ./tmp/artman/3923f78f-df98-4123-a92b-28f0755c6320/googleapis/artman-genfiles/python/datacatalog-v1beta1

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

ENTRYPOINT ["python", "cleanup_datacatalog.py"]
