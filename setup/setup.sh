#!/bin/bash

# initial updates
sudo apt-get update -y
sudo apt-get upgrade -y


# anaconda setup
# wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
# bash Anaconda3-2022.10-Linux-x86_64.sh
rm Anaconda3-2022.10-Linux-x86_64.sh

# docker install
sudo apt-get install docker.io
