#!/bin/bash

# Replace <path-to-your-key-file> with the actual path to your service account key file
# KEY_FILE="<path-to-your-key-file>"
KEY_FILE="$HOME/.gc/crime-trends-explorer-user-key.json"

# Add the environment variable GOOGLE_APPLICATION_CREDENTIALS to the .bashrc file
echo "export GOOGLE_APPLICATION_CREDENTIALS=$KEY_FILE" >> ~/.bashrc

# Add the activation command to the .bashrc file
echo "gcloud auth activate-service-account --key-file=$KEY_FILE" >> ~/.bashrc

# Source the updated .bashrc file for the current terminal session
source ~/.bashrc

echo "Service account activation command has been added to .bashrc and sourced."
