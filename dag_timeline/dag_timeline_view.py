import json

from flask_appbuilder import BaseView, expose
import pendulum

from dag_timeline.timeline import get_timeline_data


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        timeline_data = get_timeline_data(pendulum.today(), pendulum.tomorrow())
        timeline_data_json = json.dumps(timeline_data, default=str)
        return self.render_template('dag_timeline/index.html', timeline_data=timeline_data_json)


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
