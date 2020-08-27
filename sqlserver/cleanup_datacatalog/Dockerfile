# docker build -t rdbms-datacatalog-cleaner .
FROM python:3.7

ENV GOOGLE_APPLICATION_CREDENTIALS=/data/sqlserver2dc-credentials.json

# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install --reinstall build-essential -y

# Debian 10 ODBC DRIVER
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17

WORKDIR /lib
COPY ./lib/datacatalog-python.tar.gz .
RUN tar -xvf ./datacatalog-python.tar.gz
RUN pip install ./tmp/artman/3923f78f-df98-4123-a92b-28f0755c6320/googleapis/artman-genfiles/python/datacatalog-v1beta1

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

ENTRYPOINT ["python", "cleanup_datacatalog.py"]
