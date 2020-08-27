# docker build -t teradata2datacatalog .
FROM python:3.7

WORKDIR /lib

RUN apt-get update && apt-get install -y libsasl2-modules libsasl2-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

ENTRYPOINT ["python", "metadata_generator.py"]
