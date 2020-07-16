#!/usr/bin/env bash

jsonfile="/etc/docker/daemon.json"
jsonfile_path="$(dirname "$jsonfile")"

# Stop docker
sudo systemctl stop docker

# Copy docker to temporary location
cp -au /var/lib/docker /var/lib/docker.bk

# Make docker directory if not already installed
[ ! -d "$jsonfile_path" ] && mkdir -p "$jsonfile_path"

if [ ! -f "$jsonfile" ]
then
	echo "Creating jsonfile with storage-driver set to overlay2"
	echo -e "{\n \"storage-driver\":\"overlay2\"\n}" | sudo tee "$jsonfile"
else 
	echo "Add or modify existing storage driver line to be: \"storage-driver\":\"overlay2\""
	read -n 1 -s -r -p "Press any key to continue after you have performed the above step."
fi

# Start docker 
sudo systemctl start docker

# Verify that the daemon is using 'overlay2' for the 'Storage Driver'
docker info
