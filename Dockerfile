FROM python:3.9

# Folder structure
RUN mkdir -p /app &&\
    mkdir -p /app/data/aus &&\
    mkdir -p /app/data/la &&\
    mkdir -p /app/data/sd

# Set working directory
WORKDIR /app

COPY requirements.txt .
COPY .env .
# In future better use volumes with path to project folder in VM
COPY crime-trends-explorer-user-key.json /.
ENV KEY_FILE="/crime-trends-explorer-user-key.json"
#COPY flows/blocks /app/flows/blocks
#COPY flows/*.py /app/flows/

# Copy the entrypoint script into the image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

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
    wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz && \
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


# Activate the service account (to access to Google Cloud services using the service account key file)
ENV GOOGLE_APPLICATION_CREDENTIALS="${KEY_FILE}"
RUN gcloud auth activate-service-account --key-file="${KEY_FILE}"


# Make ports 80, 4200 available to the world outside this container
EXPOSE 80 4200 4040


# Set entry point as bash
# Set the entrypoint script as the entrypoint for the container
#ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
ENTRYPOINT ["bash"]
# ENTRYPOINT ["python", "flows/deploy_ingest.py"]