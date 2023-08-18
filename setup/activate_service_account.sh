#!/bin/bash

# Load variables from the .env file
source .env

# KEY_FILE_PATH - the path to service account key file (from .env file)

# Add the environment variable GOOGLE_APPLICATION_CREDENTIALS to the .bashrc file
echo "export GOOGLE_APPLICATION_CREDENTIALS=$KEY_FILE_PATH" >> ~/.bashrc

# Add the activation command to the .bashrc file
echo "gcloud auth activate-service-account --key-file=$KEY_FILE_PATH" >> ~/.bashrc

# Source the updated .bashrc file for the current terminal session
source ~/.bashrc

echo "Service account activation command has been added to .bashrc and sourced."
