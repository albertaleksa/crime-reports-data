FROM python:3.9

# Folder structure
RUN mkdir -p /app &&\
    mkdir -p /app/data/aus &&\
    mkdir -p /app/data/la &&\
    mkdir -p /app/data/sd

# Set working directory
WORKDIR /app

RUN mkdir -p /root/.dbt

COPY requirements.txt .
COPY .env .
COPY profiles.yml .


# to store event log files
RUN mkdir -p /tmp/spark-events

# Install Spark and dependencies
RUN apt-get update && \
    apt-get install -y wget && \
    mkdir -p /spark && \
    cd /spark && \
    wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
    tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz && \
    rm openjdk-11.0.2_linux-x64_bin.tar.gz && \
#    wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz && \
    wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz && \
    tar xzfv spark-3.3.2-bin-hadoop3.tgz && \
    rm spark-3.3.2-bin-hadoop3.tgz

# Set environment variables for Spark and Java
ENV JAVA_HOME="/spark/jdk-11.0.2"
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV SPARK_HOME="/spark/spark-3.3.2-bin-hadoop3"
ENV PATH="${SPARK_HOME}/bin:${PATH}"
ENV PYTHONPATH="${SPARK_HOME}/python/:${PYTHONPATH}"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:${PYTHONPATH}"

# Install gsutil and download gcs-connector
RUN apt-get install -y lsb-release gnupg curl && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get install -y google-cloud-sdk && \
    mkdir -p /app/lib && \
    cd /app/lib && \
    gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar


# RUN apt-get install wget
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir


# Make ports 80, 4200 available to the world outside this container
EXPOSE 80 4200 4040


# Set entry point as bash
# Set the entrypoint script as the entrypoint for the container
ENTRYPOINT ["bash"]
