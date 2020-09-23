#!/bin/env/bash
script_path="$(dirname $(readlink -e -- "${BASH_SOURCE}"))"
export PYTHONPATH="${PYTHONPATH}:${script_path}"
export PYTHONPATH="${PYTHONPATH}:${script_path}/Modules"
export PYTHONPATH="${PYTHONPATH}:${script_path}/cogs"
