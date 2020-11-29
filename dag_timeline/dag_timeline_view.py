from flask_appbuilder import BaseView, expose

from dag_timeline.timeline import get_timeline_data


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        return self.render_template('dag_timeline/index.html', data=get_timeline_data())


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
