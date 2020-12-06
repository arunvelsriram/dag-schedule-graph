import json

import pendulum
from airflow import settings
from flask_appbuilder import BaseView, expose

from dag_schedule_graph import logger
from dag_schedule_graph.dag_schedule import get_dag_schedules, timestamp_ms


class DAGScheduleGraphView(BaseView):
    route_base = '/dag-schedule-graph'

    @expose('/')
    def list(self):
        tz = settings.TIMEZONE
        from_dttm = pendulum.today(tz=tz)
        to_dttm = pendulum.tomorrow(tz=tz)
        logger.info(f"Getting DAG schedules - from: {from_dttm} and to: {to_dttm}")
        dag_schedules = get_dag_schedules(from_dttm, to_dttm)
        return self.render_template('dag_schedule_graph/index.html',
                                    from_dttm=timestamp_ms(from_dttm),
                                    to_dttm=timestamp_ms(to_dttm),
                                    dag_schedules=json.dumps(dag_schedules))


dag_schedule_graph_view = {
    'name': 'DAG Schedule Graph',
    'category': 'Plugins',
    'view': DAGScheduleGraphView()
}
