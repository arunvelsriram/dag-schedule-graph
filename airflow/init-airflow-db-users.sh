#!/usr/bin/env bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER airflow WITH PASSWORD 'airflow';
    CREATE DATABASE airflow;
    GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

    CREATE USER airflow_rbac WITH PASSWORD 'airflow_rbac';
    CREATE DATABASE airflow_rbac;
    GRANT ALL PRIVILEGES ON DATABASE airflow_rbac TO airflow_rbac;
EOSQL
