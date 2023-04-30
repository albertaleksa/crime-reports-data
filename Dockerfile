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
COPY crime-trends-explorer-user-key.json /.
COPY flows /app/flows

# Copy the entrypoint script into the image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


# RUN apt-get install wget
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

# CMD ["prefect", "orion", "start"]

# RUN prefect orion start &

# RUN python flows/blocks/make_gcp_blocks.py
# ENTRYPOINT ["python", "prefect/flows/deploy_ingest.py"]


# Set entry point as bash
# Set the entrypoint script as the entrypoint for the container
ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
#ENTRYPOINT ["bash"]
# ENTRYPOINT ["python", "flows/deploy_ingest.py"]