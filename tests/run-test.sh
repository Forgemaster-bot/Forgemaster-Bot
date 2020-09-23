#!/usr/bin/env bash
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"

## Bring up sql container
cd "$script_path/sqlserver"
docker-compose up -d
cd "$script_path"

## WORKAROUND UNTIL HAVE SCRIPT WHICH WAITS FOR CONTAINER TO START
#sleep 10

#############################################################################################
# Copy from templates, replacing '<SQL_PASSWORD>' and '<SQL_IP_ADDRESS>' with sql server info
#############################################################################################
templates_path="${script_path}/templates"

credentials_path="${script_path}/Credentials"
mkdir -p "$credentials_path"
cp -r "$templates_path"/* "$credentials_path"

## Set config paths
# TODO: Rename PATH to 'FILE'
export FORGEMASTER_CONFIG_PATH="${credentials_path}/config.json"
export FORGEMASTER_BOT_CONFIG_PATH="${credentials_path}/BotConfig.json"

## Replace config password/ip_addr
source "${script_path}/sqlserver/scripts/docker-sql-env.sh"
password="$(cat "$sql_secrets" | grep "^SA_PASSWORD" | cut -d '=' -f 2)"
ip_addr="$(${script_path}/sqlserver/scripts/get-ip-address.sh)"

sed -i -e "s/<SQL_PASSWORD>/${password}/" "$FORGEMASTER_CONFIG_PATH"
sed -i -e "s/<SQL_IP_ADDRESS>/${ip_addr}/" "$FORGEMASTER_CONFIG_PATH"

## Run pytest
pytest --log-cli-level=10

## Stop containter
#cd "$script_path/sqlserver"
#docker-compose down

