#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(dirname "$0")"

# initial updates
echo "=== Update system..."
sudo apt-get update -y
sudo apt-get upgrade -y
# Install unzip if not already installed
sudo apt-get install -y unzip
# Install make
sudo apt install make -y

# Create a directory for service-account-key
mkdir -p $HOME/.gc


# anaconda setup
echo "=== Anaconda Setup..."
bash "${SCRIPT_DIR}/install_anaconda.sh"

# docker install
echo "=== Install docker..."
sudo apt-get install -y docker.io

# Give permission to run docker commands without sudo in VM
echo "=== Give permission to run docker commands without sudo in VM..."
bash "${SCRIPT_DIR}/docker_without_sudo.sh"

# install docker-compose
echo "=== Install docker-compose..."
bash "${SCRIPT_DIR}/install_docker_compose.sh"

# install Terraform
echo "=== Install Terraform..."
bash "${SCRIPT_DIR}/install_terraform.sh"
