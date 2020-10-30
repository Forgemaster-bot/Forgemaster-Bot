#!/usr/bin/env bash
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"

${script_path}/../setup-env.sh

sql_path="$script_path/../sql-server"
## Bring up sql container
#cd "$sql_path"
#docker-compose up -d
#cd "$script_path"

## WORKAROUND UNTIL HAVE SCRIPT WHICH WAITS FOR CONTAINER TO START
#sleep 10
#$sql_path/scripts/drop-old-data.sh

##############################################################################################
## Copy from templates, replacing '<SQL_PASSWORD>' and '<SQL_IP_ADDRESS>' with sql server info
##############################################################################################
templates_path="${script_path}/../Credentials"
credentials_path="${script_path}/Credentials"

mkdir $credentials_path
cp ${templates_path}/* $credentials_path
for file in $(ls "${templates_path}/template*")
do
	target_file="${credentials_path}/${file/template-/}"
	cp "$file" "${target_file}"
done


## Set config paths
# TODO: Rename PATH to 'FILE'
export FORGEMASTER_CONFIG_PATH="${credentials_path}/config.json"
export FORGEMASTER_BOT_CONFIG_PATH="${credentials_path}/BotConfig.json"

## Replace config password/ip_addr
source "${sql_path}/scripts/docker-sql-env.sh"
password="$(cat "$sql_secrets" | grep "^SA_PASSWORD" | cut -d '=' -f 2)"
ip_addr="$(${sql_path}/scripts/get-ip-address.sh)"

sed -i -e "s/<SQL_PASSWORD>/${password}/" "$FORGEMASTER_CONFIG_PATH"
sed -i -e "s/<SQL_IP_ADDRESS>/${ip_addr}/" "$FORGEMASTER_CONFIG_PATH"

## Run pytest
#pytest --log-cli-level=10

## Stop containter
#cd "$script_path/automation/sqlserver"
#docker-compose down

