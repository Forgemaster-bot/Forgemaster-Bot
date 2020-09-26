#!/usr/bin/env bash

# source environment file to pickup user config
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"
source "${script_path}/docker-sql-env.sh"

password="$(cat "$sql_secrets" | grep "^SA_PASSWORD" | cut -d '=' -f 2)"
DB="LostWorld"

# run the command
docker exec test-server /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "$password" -d "$DB" -s "," -W -w 700 -Q "$@"

