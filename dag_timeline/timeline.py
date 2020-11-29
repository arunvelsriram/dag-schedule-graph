from typing import List

import pendulum
from airflow import settings
from airflow.models import DagModel
from croniter import croniter
from pendulum import Pendulum
from sqlalchemy.orm import Session


def get_dags() -> List[DagModel]:
    session: Session = settings.Session()
    return session.query(DagModel).all()


def get_timeline_data(from_dt: Pendulum, to_dt: Pendulum) -> List:
    dags = get_dags()

    timeline_data = []
    for dag in dags:
        data = []
        iterator = croniter(dag.schedule_interval, from_dt)
        while True:
            start = pendulum.instance(iterator.get_next(pendulum.datetime))
            end = start.add(hours=1)
            if start >= to_dt:
                break
            data.append({"timeRange": [start, end], "val": dag.dag_id})

        if len(data) > 0:
            timeline_data.append({"label": dag.dag_id, "data": data})

    return [{"group": "", "data": timeline_data}]
