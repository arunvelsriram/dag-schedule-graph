from datetime import timedelta
from unittest.mock import patch

from airflow import DAG
from pendulum import datetime as pendulum_datetime

from dag_schedule_graph.dag_schedule import get_dag_schedules, get_qualified_dags


class TestDAGSchedule:

    @patch('dag_schedule_graph.dag_schedule.DagBag')
    def test_get_qualified_dags(self, mock_dag_bag):
        test_dag_1 = DAG('test-dag-1', start_date=pendulum_datetime(2020, 1, 1))
        test_dag_2 = DAG('test-dag-2', start_date=pendulum_datetime(2020, 1, 2))
        test_dag_3 = DAG('test-dag-2', start_date=pendulum_datetime(2020, 1, 3))
        mock_dag_bag.return_value.dags = {
            'test-dag-1': test_dag_1,
            'test-dag-2': test_dag_2,
            'test-dag-3': test_dag_3,
        }
        base_dt = pendulum_datetime(2020, 1, 2)

        dags = get_qualified_dags(base_dt)

        assert dags == [test_dag_1, test_dag_2]

    @patch('dag_schedule_graph.dag_schedule.DagBag')
    def test_get_qualified_dags_should_skip_sub_dags(self, mock_dag_bag):
        base_dt = pendulum_datetime(2020, 1, 2)
        test_dag = DAG('test-dag')
        test_dag.is_subdag = True
        mock_dag_bag.return_value.dags = {'test-dag': test_dag}

        dags = get_qualified_dags(base_dt)

        assert dags == []

    @patch('dag_schedule_graph.dag_schedule.DagBag')
    def test_get_qualified_dags_should_skip_dags_with_schedule_interval_none(self, mock_dag_bag):
        base_dt = pendulum_datetime(2020, 1, 2)
        test_dag = DAG('test-dag', schedule_interval=None)
        mock_dag_bag.return_value.dags = {'test-dag': test_dag}

        dags = get_qualified_dags(base_dt)

        assert dags == []

    @patch('dag_schedule_graph.dag_schedule.DagBag')
    def test_get_qualified_dags_should_skip_dags_with_future_start_date(self, mock_dag_bag):
        base_dt = pendulum_datetime(2020, 1, 2)
        test_dag = DAG('test-dag', start_date=pendulum_datetime(3020, 1, 1))
        mock_dag_bag.return_value.dags = {'test-dag': test_dag}

        dags = get_qualified_dags(base_dt)

        assert dags == []

    @patch('dag_schedule_graph.dag_schedule.DagBag')
    def test_get_qualified_dags_should_skip_dags_with_future_start_date_in_default_args(self, mock_dag_bag):
        base_dt = pendulum_datetime(2020, 1, 2)
        test_dag = DAG('test-dag-1', default_args={"start_date": pendulum_datetime(3020, 1, 1)})
        mock_dag_bag.return_value.dags = {'test_dag': test_dag}

        dags = get_qualified_dags(base_dt)

        assert dags == []

    @patch('dag_schedule_graph.dag_schedule.get_qualified_dags')
    def test_get_dag_schedule_for_cron_expression(self, mock_get_qualified_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_qualified_dags.return_value = [
            DAG('test-dag-1', start_date=from_dt, schedule_interval='0 */8 * * *')
        ]

        expected = [{'dag_id': 'test-dag-1',
                     'schedules': [pendulum_datetime(2020, 1, 1, 0).timestamp() * 1000,
                                   pendulum_datetime(2020, 1, 1, 8).timestamp() * 1000,
                                   pendulum_datetime(2020, 1, 1, 16).timestamp() * 1000,
                                   pendulum_datetime(2020, 1, 2, 0).timestamp() * 1000]}]
        assert get_dag_schedules(from_dt, to_dt) == expected

    @patch('dag_schedule_graph.dag_schedule.get_qualified_dags')
    def test_get_dag_schedule_for_airflow_cron_preset(self, mock_get_qualified_dags):
        from_dt = pendulum_datetime(2020, 1, 5)
        to_dt = pendulum_datetime(2020, 1, 6)
        mock_get_qualified_dags.return_value = [
            DAG(dag_id='test-dag-1', start_date=from_dt, schedule_interval='@weekly'),
        ]

        expected = [{'dag_id': 'test-dag-1',
                     'schedules': [pendulum_datetime(2020, 1, 5, 0).timestamp() * 1000]}]
        assert get_dag_schedules(from_dt, to_dt) == expected

    @patch('dag_schedule_graph.dag_schedule.get_qualified_dags')
    def test_get_dag_schedule_for_timedelta(self, mock_get_qualified_dags):
        from_dt = pendulum_datetime(2020, 1, 1)
        to_dt = pendulum_datetime(2020, 1, 2)
        mock_get_qualified_dags.return_value = [
            DAG(dag_id='test-dag-1', start_date=from_dt, schedule_interval=timedelta(hours=8)),
        ]

        expected = [{'dag_id': 'test-dag-1',
                     'schedules': [pendulum_datetime(2020, 1, 1, 0).timestamp() * 1000,
                                   pendulum_datetime(2020, 1, 1, 8).timestamp() * 1000,
                                   pendulum_datetime(2020, 1, 1, 16).timestamp() * 1000,
                                   pendulum_datetime(2020, 1, 2, 0).timestamp() * 1000]}]
        assert get_dag_schedules(from_dt, to_dt) == expected
