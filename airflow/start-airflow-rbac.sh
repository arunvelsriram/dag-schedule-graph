#!/usr/bin/env bash

set -e

airflow initdb
airflow create_user -u admin -e admin@gmail.com -p admin -f admin -l admin -r Admin
airflow scheduler &
airflow webserver
