import json

import pendulum
from airflow import settings
from flask_appbuilder import BaseView, expose

from dag_timeline import logger
from dag_timeline.timeline import get_timeline_data


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        tz = settings.TIMEZONE
        from_dt = pendulum.today(tz=tz)
        to_dt = pendulum.tomorrow(tz=tz)
        logger.info(f"Getting timeline data from {from_dt} to {to_dt}")
        timeline_data = get_timeline_data(from_dt, to_dt)
        timeline_data_json = json.dumps(timeline_data, default=str)
        return self.render_template('dag_timeline/index.html', timeline_data=timeline_data_json)


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
