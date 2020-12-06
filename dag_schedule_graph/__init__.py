from airflow.plugins_manager import AirflowPlugin
from airflow.settings import RBAC
from flask import Blueprint

from dag_schedule_graph.log import logger

bp = Blueprint('dag_schedule_graph',
               __name__,
               url_prefix='/dag-schedule-graph',
               template_folder='templates',
               static_folder='static')
appbuilder_views = []

if RBAC:
    from dag_schedule_graph.dag_schedule_graph_view import dag_schedule_graph_view

    appbuilder_views = [dag_schedule_graph_view]
else:
    logger.error('dag-schedule-graph plugin works only on FAB based RBAC UI')


class DAGScheduleGraphPlugin(AirflowPlugin):
    name = 'dag_schedule_graph'
    flask_blueprints = [bp]
    appbuilder_views = appbuilder_views
