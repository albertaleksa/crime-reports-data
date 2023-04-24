#!/bin/bash

# Anaconda setup

echo "=== Run install_anaconda.sh..."
echo "=== Download Anaconda..."
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh

# if Anaconda is already installed, update it
if [ -d "$HOME/anaconda3" ]; then
    echo "=== Anaconda is already installed. Updating Anaconda..."
    bash Anaconda3-2022.10-Linux-x86_64.sh -u -b
else
    # install Anaconda in batch mode (non-interactive)
    echo "=== Install Anaconda..."
    bash Anaconda3-2022.10-Linux-x86_64.sh -b
fi

# clean up
echo "=== Remove installation file for Anaconda..."
rm Anaconda3-2022.10-Linux-x86_64.sh
