#!/usr/bin/env bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test-server
