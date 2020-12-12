import json

import pendulum
from flask_appbuilder import BaseView, expose

from dag_schedule_graph import logger
from dag_schedule_graph.dag_schedule import get_dag_schedules, timestamp_ms


class DAGScheduleGraphView(BaseView):
    route_base = '/dag-schedule-graph'

    @expose('/')
    def list(self):
        utc = pendulum.timezone('UTC')
        from_dttm = pendulum.today(tz=utc)
        to_dttm = pendulum.tomorrow(tz=utc)
        logger.info(f'Getting DAG schedules - from: {from_dttm} and to: {to_dttm}')
        dag_schedules = get_dag_schedules(from_dttm, to_dttm)
        return self.render_template('dag_schedule_graph/index.html',
                                    from_timestamp=timestamp_ms(from_dttm),
                                    to_timestamp=timestamp_ms(to_dttm),
                                    dag_schedules=json.dumps(dag_schedules))


dag_schedule_graph_view = {
    'name': 'DAG Schedule Graph',
    'category': 'Plugins',
    'view': DAGScheduleGraphView()
}
