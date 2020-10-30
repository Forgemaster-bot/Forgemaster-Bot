
You must have `docker` and `docker-compose` installed.

To run tests run the following from this directory:
` docker-compose -f unit-test-compose.yml up --build --abort-on-container-exit `
Note: You may have issues due to it being the first time setting up the sql repository... You may need to rerun it after the first time.

=======
Dependencies:
- python3.8
- python3-distutils
- python3-dev
- python3-pip
- gcc
- [mssql driver](https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15)
- `Forgemaster-Bot`, `Forgemaster-Bot/Modules`, and `Forgemaster/cogs` added to PYTHONPATH environment variable.

With dependencies installed do the following:
1. `pip install -r requirements.txt`
2. `python launcher.py`

