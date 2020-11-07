import logging

from airflow.plugins_manager import AirflowPlugin
from airflow.settings import RBAC
from flask import Blueprint

plugin_name = 'dag_timeline'
logger = logging.getLogger(plugin_name)
bp = Blueprint(plugin_name,
               __name__,
               template_folder='templates')
appbuilder_views = []

if RBAC:
    from dag_timeline.dag_timeline_view import dag_timeline_view

    appbuilder_views = [dag_timeline_view]
else:
    logger.error('dag-timeline plugin works only on FAB based RBAC UI')


class DAGTimelinePlugin(AirflowPlugin):
    name = plugin_name
    flask_blueprints = [bp]
    appbuilder_views = appbuilder_views
