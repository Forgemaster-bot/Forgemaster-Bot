#!/usr/bin/env bash
sudo apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc
sudo cp freetds.conf /etc/freetds
sudo cp odbc.ini /etc
sudo cp odbcinst.ini /etc
