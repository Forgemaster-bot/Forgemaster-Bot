#!/usr/bin/env bash

image="mcr.microsoft.com/mssql/server:2019-CU5-ubuntu-18.04"

# Pull image from public docker registry
sudo docker pull "$image"

