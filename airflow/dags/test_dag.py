from builtins import range

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

args = {
    'owner': 'Airflow',
    'start_date': days_ago(2),
}

dag1 = DAG(
    dag_id='test_dag1',
    default_args=args,
    schedule_interval='0 */2 * * *',
    tags=['example']
)

run_this_last = DummyOperator(
    task_id='run_this_last',
    dag=dag1,
)

run_this = BashOperator(
    task_id='run_after_loop',
    bash_command='echo 1',
    dag=dag1,
)

run_this >> run_this_last

for i in range(3):
    task = BashOperator(
        task_id='runme_' + str(i),
        bash_command='echo "{{ task_instance_key_str }}" && sleep 1',
        dag=dag1,
    )
    task >> run_this

also_run_this = BashOperator(
    task_id='also_run_this',
    bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"',
    dag=dag1,
)
also_run_this >> run_this_last

dag2 = DAG(
    dag_id='test_dag2',
    default_args=args,
    schedule_interval='0 */1 * * *',
    tags=['example']
)

t1 = BashOperator(
    task_id='test_dag2_hi',
    bash_command="echo Hi",
    dag=dag2
)

t2 = BashOperator(
    task_id='test_dag2_bye',
    bash_command="echo Bye",
    dag=dag2
)

t1 >> t2

dag3 = DAG(
    dag_id='test_dag3',
    default_args=args,
    schedule_interval='0 */1 * * *',
    tags=['example']
)

t3 = BashOperator(
    task_id='test_dag3_hi',
    bash_command="echo Hi",
    dag=dag2
)

t4 = BashOperator(
    task_id='test_dag3_bye',
    bash_command="echo Bye",
    dag=dag2
)

t3 >> t4
