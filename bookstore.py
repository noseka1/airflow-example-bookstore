from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.contrib.sensors.file_sensor import FileSensor

import json
from builtins import range
from datetime import timedelta

args = {
    'owner': 'user',
    'start_date': days_ago(1),
}

dag = DAG(
    dag_id='bookstore',
    default_args=args,
    schedule_interval='0 0 * * *',
    dagrun_timeout=timedelta(minutes=60),
    tags=['bookstore']
)

def push_rate_func(**kwargs):
    filename='/tmp/bookstore/rate-%s.json' % (kwargs.get('ds'))
    with open(filename) as f:
        data = json.load(f)
    kwargs['ti'].xcom_push(key=None, value=data['rate'])

def compute_revenue_func(**kwargs):
    filename='/tmp/bookstore/revenue-%s.json' % (kwargs.get('ds'))
    with open(filename) as f:
        data = json.load(f)
    revenue = data['revenue']

    ti = kwargs['ti']
    rate = ti.xcom_pull(key=None, task_ids='push_rate')

    converted_revenue = {
        "revenue": revenue * rate
    }
    filename='/tmp/bookstore/revenue-report-%s.json' % (kwargs.get('ds'))
    with open(filename, 'w') as f:
        json.dump(converted_revenue, f)

wait_for_revenue = FileSensor(
    filepath='/tmp/bookstore/revenue-{{ ds }}.json',
    task_id='wait_for_revenue',
    dag=dag,
)

wait_for_rate = FileSensor(
    filepath='/tmp/bookstore/rate-{{ ds }}.json',
    task_id='wait_for_rate',
    dag=dag,
)

push_rate = PythonOperator(
    task_id='push_rate',
    provide_context=True,
    python_callable=push_rate_func,
    dag=dag,
)

compute_report = PythonOperator(
    task_id='compute_report',
    provide_context=True,
    python_callable=compute_revenue_func,
    dag=dag,
)

wait_for_revenue >> compute_report
wait_for_rate >> push_rate >> compute_report

if __name__ == "__main__":
    dag.cli()
