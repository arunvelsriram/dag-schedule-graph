from typing import List, Optional

import pendulum
from airflow import DAG
from airflow.models import DagBag
from pendulum import Pendulum

from dag_timeline import logger


def get_dags() -> List[DAG]:
    dags = []
    for dag_id, dag in DagBag().dags.items():
        dags.append(dag)
    return dags


def is_future_date(dt: Pendulum, base_dt: Pendulum) -> bool:
    if dt and dt > base_dt:
        return True
    return False


def is_future_start_date(dag: DAG, base_dt: Pendulum):
    return is_future_date(dag.start_date, base_dt) or \
           is_future_date(dag.default_args.get('start_date'), base_dt)


def get_timeline_data(from_dt: Pendulum, to_dt: Pendulum):
    logger.info('Getting all DAGs')
    dags = get_dags()
    timeline_data = []
    for dag in dags:
        logger.debug(f'dag_id: {dag.dag_id}, start_date:{dag.start_date}, schedule_interval: {dag.schedule_interval}')
        if dag.schedule_interval is None:
            logger.info(f'Skip processing {dag.dag_id} as it has no schedule_interval')
            continue
        if is_future_start_date(dag, to_dt):
            logger.info(f'Skip processing {dag.dag_id} as it has a future start_date')
            continue
        data = []
        logger.debug(f'Getting run dates for {dag.dag_id}')
        for run_date in dag.get_run_dates(from_dt, to_dt):
            start = pendulum.instance(run_date)
            end = start.add(hours=1)
            data.append({'timeRange': [start, end], 'val': dag.dag_id})

        if len(data) > 0:
            logger.info(f'Skip adding {dag.dag_id} to timeline data as it has no runs')
            timeline_data.append({'label': dag.dag_id, 'data': data})

    return [{'group': '', 'data': timeline_data}]
