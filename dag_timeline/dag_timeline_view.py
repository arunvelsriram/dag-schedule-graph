import json

import pendulum
from airflow import settings
from flask_appbuilder import BaseView, expose

from dag_timeline import logger
from dag_timeline.timeline import get_dag_schedules


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        tz = settings.TIMEZONE
        from_dt = pendulum.today(tz=tz)
        to_dt = pendulum.tomorrow(tz=tz)
        logger.info(f"Getting DAG schedules - from: {from_dt} and to: {to_dt}")
        dag_schedules = get_dag_schedules(from_dt, to_dt)
        return self.render_template('dag_timeline/index.html', dag_schedules=json.dumps(dag_schedules))


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
