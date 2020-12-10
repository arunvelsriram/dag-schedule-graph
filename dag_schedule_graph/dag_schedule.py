from typing import Dict, List

import pendulum
from airflow import DAG
from airflow.models import DagBag
from pendulum import Pendulum

from dag_schedule_graph import logger


def is_future_date(dt: Pendulum, base_dt: Pendulum) -> bool:
    if dt and dt > base_dt:
        return True
    return False


def is_future_start_date(dag: DAG, base_dt: Pendulum):
    return is_future_date(dag.start_date, base_dt) or \
           is_future_date(dag.default_args.get('start_date'), base_dt)


def timestamp_ms(dt: Pendulum):
    return dt.timestamp() * 1000


def get_qualified_dags(base_dt: Pendulum) -> List[DAG]:
    def check(dag_id, dag):
        if dag.is_subdag:
            logger.info(f'Skipping sub DAG: {dag_id}')
            return False
        if dag.schedule_interval is None:
            logger.info(f'Skipping DAG with schedule_interval None: {dag_id}')
            return False
        if is_future_start_date(dag, base_dt):
            logger.info(f'Skipping DAG with future start_date: {dag_id}')
            return False
        return True

    return [dag for dag_id, dag in DagBag().dags.items() if check(dag_id, dag)]


DAGSchedule = Dict[float, List[str]]


def get_dag_schedules(from_dttm: Pendulum, to_dttm: Pendulum) -> DAGSchedule:
    logger.info('Getting qualified DAGs')
    dags = get_qualified_dags(to_dttm)
    dag_schedules = {}
    for dag in dags:
        logger.debug(
            f'DAG - dag_id: {dag.dag_id}, start_date: {dag.start_date}, schedule_interval: {dag.schedule_interval}')
        for run_date in dag.get_run_dates(from_dttm, to_dttm):
            start = pendulum.instance(run_date)
            start_ms = timestamp_ms(start)
            dag_ids = dag_schedules.setdefault(start_ms, [])
            dag_ids.append(dag.dag_id)

    return dag_schedules
