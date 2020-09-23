#!/usr/bin/env bash
script_loc="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"
export sql_image="mcr.microsoft.com/mssql/server:2019-CU5-ubuntu-18.04"
export sql_secrets="${script_loc}/.sql_secrets"
export sql_container_name="sql1"
export sql_port="1433:1433"
