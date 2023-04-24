#!/bin/bash

# Install docker-compose

echo "=== Run install_docker_compose.sh..."

# Create a directory for executable files if it doesn't exist
mkdir -p $HOME/bin

# Download docker-compose into the bin directory
echo "=== Download docker-compose..."
wget https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64 -O $HOME/bin/docker-compose

# Make docker-compose executable
echo "=== Make docker-compose executable..."
chmod +x $HOME/bin/docker-compose

# Add the bin directory to the PATH variable if it's not already there
echo "=== Make docker-compose visible from any directory..."
grep -qxF 'export PATH="${HOME}/bin:${PATH}"' $HOME/.bashrc || echo 'export PATH="${HOME}/bin:${PATH}"' >> $HOME/.bashrc

# Reload .bashrc
echo "=== Reload .bashrc..."
source $HOME/.bashrc
