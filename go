#!/usr/bin/env bash

set -e

pushd airflow
docker-compose up -d --force-recreate airflow-rbac
docker-compose logs -f
popd
