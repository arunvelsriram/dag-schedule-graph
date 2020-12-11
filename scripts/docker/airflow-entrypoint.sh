#!/usr/bin/env bash

set -e

#echo "==> Installing dag-schedule-graph plugin"
#pip install /opt/dag-schedule-graph

echo "==> Initializing DB"
airflow db init

echo "Creating admin user"
airflow users create -u admin -e admin@gmail.com -p admin \
  -f admin -l admin -r Admin

echo "==> Starting scheduler"
airflow scheduler &

echo "==> Starting webserver"
airflow webserver
