from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from flask_appbuilder import BaseView, expose

PLUGIN_NAME = 'dag_timeline'


class DAGTimelineView(BaseView):
    route_base = '/admin/aaa'

    @expose("/")
    def list(self):
        return self.render_template("test_plugin/test.html", content="Hello galaxy!")


view = {
    "name": "DAG Timeline",
    "category": "Plugins",
    "view": DAGTimelineView()
}

bp = Blueprint(
    PLUGIN_NAME,
    __name__,
    template_folder='templates'
)


class DAGTimelinePlugin(AirflowPlugin):
    name = PLUGIN_NAME
    flask_blueprints = [bp]
    appbuilder_views = [view]
