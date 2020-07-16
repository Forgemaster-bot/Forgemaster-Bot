#!/usr/bin/env bash
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"
# source environment file to pickup user config
source "${script_path}/docker-sql-env.sh"
# run the image
docker start $sql_container_name"
