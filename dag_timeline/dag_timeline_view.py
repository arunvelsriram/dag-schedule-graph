from flask_appbuilder import BaseView, expose


class DAGTimelineView(BaseView):
    route_base = '/dag-timeline'

    @expose('/')
    def list(self):
        testData = [
            {
                "times": [
                    {"starting_time": 1355752800000, "ending_time": 1355759900000},
                    {"starting_time": 1355767900000, "ending_time": 1355774400000}
                ]
            },
            {"times": [{"starting_time": 1355759910000, "ending_time": 1355761900000}]},
            {"times": [{"starting_time": 1355761910000, "ending_time": 1355763910000}]}
        ]
        return self.render_template('dag_timeline/index.html', data=testData)


dag_timeline_view = {
    'name': 'DAG Timeline',
    'category': 'Plugins',
    'view': DAGTimelineView()
}
