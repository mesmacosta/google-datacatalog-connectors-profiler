# docker build -t sqlserver2datacatalog .
FROM python:3.7

ENV ORACLE_HOME=/opt/oracle/instantclient_19_5
ENV LD_LIBRARY_PATH=$ORACLE_HOME
ENV LD_RUN_PATH=$ORACLE_HOME

RUN curl https://download.oracle.com/otn_software/linux/instantclient/195000/instantclient-basic-linux.x64-19.5.0.0.0dbru.zip > instantclient-basic-linux.x64-19.5.0.0.0dbru.zip
RUN mkdir -p /opt/oracle && \
unzip "instantclient*.zip" -d /opt/oracle && \
ln -s $ORACLE_HOME 

RUN apt-get update \
 && apt-get install libaio1 -y 

WORKDIR /lib
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

# Copy project files (see .dockerignore).
COPY . .

ENTRYPOINT ["python", "metadata_generator.py"]
