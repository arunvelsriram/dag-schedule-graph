# DAG Schedule Graph


## Development

```
conda create -n dag-schedule-graph python=3.7.9
source .envrc
pip install -e '.[dev]'
airflow initdb
airflow create_user -u admin -e admin@gmail.com -p admin -f admin -l admin -r Admin
airflow webserver
```
