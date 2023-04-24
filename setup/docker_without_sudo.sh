#!/bin/sh

# Give permission to run docker commands without sudo in VM

echo "=== Run docker_without_sudo.sh..."

# 1. Add the docker group if it doesn't already exist
echo "=== Add the docker group..."
sudo groupadd docker

# 2. Add the connected user $USER to the docker group
# Optionally change the username to match your preferred user.
echo "=== Add user $USER to the docker group..."
sudo gpasswd -a "$USER" docker

# 3. Restart the docker daemon
echo "=== Restart the docker daemon..."
if command -v service >/dev/null; then
  if [ "$(lsb_release -cs)" = "trusty" ] || [ "$(lsb_release -cs)" = "wily" ]; then
    sudo service docker.io restart
  else
    sudo service docker restart
  fi
else
  sudo systemctl restart docker
fi

echo "=== IMPORTANT: Log out and log back in so that your group membership is re-evaluated."
