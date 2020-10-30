#!/usr/bin/env bash

# source environment file to pickup user config
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"
source "${script_path}/docker-sql-env.sh"

password="$(cat "$sql_secrets" | grep "^SA_PASSWORD" | cut -d '=' -f 2)"

# run the image 
docker exec -it test-server /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$password" -Q "
 USE LostWorld;
 DELETE FROM Main_Crafting;
 "
 
