#!/bin/bash

# Run Prefect Orion in background
prefect orion start &

# Sleep for 30 seconds
sleep 30

# Run Agent in background
prefect agent start --work-queue "default" &

sleep 10

# Run python script to create blocks fo Prefect
python flows/blocks/make_gcp_blocks.py

# Start a new bash shell for interaction
exec bash