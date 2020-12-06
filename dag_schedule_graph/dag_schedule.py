from typing import Dict, List, Union

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


DAGSchedule = List[Dict[str, Union[str, List[float]]]]


def get_dag_schedules(from_dt: Pendulum, to_dt: Pendulum) -> DAGSchedule:
    logger.info('Getting qualified DAGs')
    dags = get_qualified_dags(to_dt)
    dag_schedules = []
    for dag in dags:
        logger.debug(
            f'DAG - dag_id: {dag.dag_id}, start_date: {dag.start_date}, schedule_interval: {dag.schedule_interval}')
        schedules = []
        logger.debug(f'Getting schedules {dag.dag_id}')
        for run_date in dag.get_run_dates(from_dt, to_dt):
            start = pendulum.instance(run_date)
            start_ms = timestamp_ms(start)
            schedules.append(start_ms)

        if len(schedules) > 0:
            logger.info(f'Skipping DAG with no schedules: {dag.dag_id}')
            dag_schedules.append({'dag_id': dag.dag_id, 'schedules': schedules})

    return dag_schedules
