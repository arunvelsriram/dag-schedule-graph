# DAG Timeline


## Development

```
conda env create -n dag-timeline python=3.7.9
source .envrc
airflow initdb
airflow create_user -u admin -e admin@gmail.com -p admin -f admin -l admin -r Admin
pip install -e '.[dev]'
airflow webserver
```
