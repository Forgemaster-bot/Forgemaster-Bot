#!/usr/bin/env bash

# Create the docker group
sudo groupadd docker

# Add youself to the docker group
sudo usermod -aG docker $USER

# Refresh groups
newgrp docker

# Check if you can run docker hello-world
docker run hello-world
