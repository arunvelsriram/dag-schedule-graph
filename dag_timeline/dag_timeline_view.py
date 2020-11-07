from flask_appbuilder import BaseView, expose


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        return self.render_template('dag_timeline/index.html')


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
