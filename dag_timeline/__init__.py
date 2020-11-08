from airflow.plugins_manager import AirflowPlugin
from airflow.settings import RBAC
from flask import Blueprint

from dag_timeline.log import logger

bp = Blueprint('dag_timeline',
               __name__,
               url_prefix='/dag-timeline',
               template_folder='templates',
               static_folder='static')
appbuilder_views = []

if RBAC:
    from dag_timeline.dag_timeline_view import dag_timeline_view

    appbuilder_views = [dag_timeline_view]
else:
    logger.error('dag-timeline plugin works only on FAB based RBAC UI')


class DAGTimelinePlugin(AirflowPlugin):
    name = 'dag_timeline'
    flask_blueprints = [bp]
    appbuilder_views = appbuilder_views
