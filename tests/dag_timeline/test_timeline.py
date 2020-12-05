from datetime import timedelta
from unittest.mock import patch

from airflow import DAG
from pendulum import datetime as pendulum_datetime

from dag_timeline.timeline import get_timeline_data, get_dags


class TestTimeline:

    @patch('dag_timeline.timeline.DagBag')
    def test_get_dags(self, mock_dag_bag):
        test_dag_1 = DAG('test-dag-1', start_date=pendulum_datetime(2020, 1, 1))
        test_dag_2 = DAG('test-dag-2', start_date=pendulum_datetime(2020, 1, 2))
        mock_dag_bag.return_value.dags = {
            'test-dag-1': test_dag_1,
            'test-dag-2': test_dag_2
        }

        dags = get_dags()

        assert len(dags) == 2
        assert dags == [test_dag_1, test_dag_2]

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data_should_skip_dags_with_schedule_interval_none(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_dags.return_value = [
            DAG('test-dag-1', schedule_interval=None)
        ]

        assert get_timeline_data(from_dt, to_dt) == [{'group': '', 'data': []}]

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data_should_skip_dags_with_future_start_date(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_dags.return_value = [
            DAG('test-dag-1', start_date=pendulum_datetime(3020, 1, 1))
        ]

        assert get_timeline_data(from_dt, to_dt) == [{'group': '', 'data': []}]

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data_should_skip_dags_with_future_start_date_in_default_args(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_dags.return_value = [
            DAG('test-dag-1', default_args={"start_date": pendulum_datetime(3020, 1, 1)})
        ]

        assert get_timeline_data(from_dt, to_dt) == [{'group': '', 'data': []}]

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data_for_cron_expression(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_dags.return_value = [
            DAG('test-dag-1', start_date=from_dt, schedule_interval='0 */8 * * *')
        ]

        expected = [{
            'group': '',
            'data': [{
                'label': 'test-dag-1',
                'data': [{
                    'timeRange': [pendulum_datetime(2020, 1, 1, 0), pendulum_datetime(2020, 1, 1, 1)],
                    'val': 'test-dag-1'
                }, {
                    'timeRange': [pendulum_datetime(2020, 1, 1, 8), pendulum_datetime(2020, 1, 1, 9)],
                    'val': 'test-dag-1'
                }, {
                    'timeRange': [pendulum_datetime(2020, 1, 1, 16), pendulum_datetime(2020, 1, 1, 17)],
                    'val': 'test-dag-1'
                }, {
                    'timeRange': [pendulum_datetime(2020, 1, 2, 0), pendulum_datetime(2020, 1, 2, 1)],
                    'val': 'test-dag-1'
                }]
            }]
        }]
        assert get_timeline_data(from_dt, to_dt) == expected

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data_for_airflow_cron_preset(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 5)
        to_dt = pendulum_datetime(2020, 1, 6)
        mock_get_dags.return_value = [
            DAG(dag_id='test-dag-1', start_date=from_dt, schedule_interval='@weekly'),
        ]
        expected = [{
            'group': '',
            'data': [{
                'label': 'test-dag-1',
                'data': [{
                    'timeRange': [pendulum_datetime(2020, 1, 5, 0), pendulum_datetime(2020, 1, 5, 1)],
                    'val': 'test-dag-1'
                }]
            }]
        }]
        assert get_timeline_data(from_dt, to_dt) == expected

    @patch('dag_timeline.timeline.get_dags')
    def test_get_data_for_timedelta(self, mock_get_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_dags.return_value = [
            DAG(dag_id='test-dag-1', start_date=from_dt, schedule_interval=timedelta(hours=8)),
        ]
        expected = [{
            'group': '',
            'data': [{
                'label': 'test-dag-1',
                'data': [{
                    'timeRange': [pendulum_datetime(2020, 1, 1, 0), pendulum_datetime(2020, 1, 1, 1)],
                    'val': 'test-dag-1'
                }, {
                    'timeRange': [pendulum_datetime(2020, 1, 1, 8), pendulum_datetime(2020, 1, 1, 9)],
                    'val': 'test-dag-1'
                }, {
                    'timeRange': [pendulum_datetime(2020, 1, 1, 16), pendulum_datetime(2020, 1, 1, 17)],
                    'val': 'test-dag-1'
                }, {
                    'timeRange': [pendulum_datetime(2020, 1, 2, 0), pendulum_datetime(2020, 1, 2, 1)],
                    'val': 'test-dag-1'
                }]
            }]
        }]
        assert get_timeline_data(from_dt, to_dt) == expected
