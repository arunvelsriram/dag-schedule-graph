import json

import pendulum
from airflow import settings
from flask_appbuilder import BaseView, expose

from dag_timeline import logger
from dag_timeline.timeline import get_dag_schedules, timestamp_ms


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        tz = settings.TIMEZONE
        from_dttm = pendulum.today(tz=tz)
        to_dttm = pendulum.tomorrow(tz=tz)
        logger.info(f"Getting DAG schedules - from: {from_dttm} and to: {to_dttm}")
        dag_schedules = get_dag_schedules(from_dttm, to_dttm)
        return self.render_template('dag_timeline/index.html',
                                    from_dttm=timestamp_ms(from_dttm),
                                    to_dttm=timestamp_ms(to_dttm),
                                    dag_schedules=json.dumps(dag_schedules))


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
