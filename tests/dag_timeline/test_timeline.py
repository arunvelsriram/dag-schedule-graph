from unittest.mock import patch

from airflow.models import DagModel
from pendulum import datetime as pendulum_datetime

from dag_timeline.timeline import get_timeline_data, get_dags


class TestTimeline:

    def test_get_dags(self):
        dags = get_dags()
        assert len(dags) > 0

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_dags.return_value = [
            DagModel(dag_id='test-dag-1', schedule_interval='0 15,18 * * *'),
            DagModel(dag_id='test-dag-1', schedule_interval='0 */8 5 * *')
        ]
        expected = [{
            "group": "",
            "data": [{
                "label": "test-dag-1",
                "data": [{
                    "timeRange": [pendulum_datetime(2020, 1, 1, 15), pendulum_datetime(2020, 1, 1, 16)],
                    "val": "test-dag-1"
                }, {
                    "timeRange": [pendulum_datetime(2020, 1, 1, 18), pendulum_datetime(2020, 1, 1, 19)],
                    "val": "test-dag-1"
                }]
            }]
        }]
        assert get_timeline_data(from_dt, to_dt) == expected

