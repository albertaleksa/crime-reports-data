#!/bin/bash

# Install Terraform

echo "=== Run install_terraform.sh..."

cd tmp

# Download Terraform
echo "=== Download Terraform..."
wget https://releases.hashicorp.com/terraform/1.3.9/terraform_1.3.9_linux_amd64.zip

# Unzip Terraform archive
echo "=== Unzip Terraform archive..."
unzip terraform_1.3.9_linux_amd64.zip

# Move the Terraform binary to the bin directory
echo "=== Move the Terraform binary to the bin directory..."
mv terraform $HOME/bin/

# Remove the downloaded zip file
echo "=== Remove the downloaded zip file..."
rm terraform_1.3.9_linux_amd64.zip
