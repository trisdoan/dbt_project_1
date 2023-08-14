from datetime import datetime, timedelta

##Airflow import###
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from src.extract_data import (
    extract_customer_data,
    extract_order_data,
    load_customer_data,
    load_order_data,
)

# Config
# DBT_PROJECT_DIR  = Variable.get('DBT_PROJECT_DIR')
# DBT_PROFILES_DIR = Variable.get('DBT_PROFILES_DIR')

# DAG Definition
default_args = {
    "owner": "warehouse",
    "start_date": datetime(2023, 8, 10),
    "wait_for_downstream": True,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}
dag = DAG(
    "elt_online_store",
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
)

extract_load_order_data = PythonOperator(
    dag=dag,
    task_id="extract_load_order_data",
    python_callable=load_order_data,
    op_kwargs={'order_data': extract_order_data()},
)

extract_load_customer_data = PythonOperator(
    dag=dag,
    task_id="extract_load_customer_data",
    python_callable=load_customer_data,
    op_kwargs={'customer_data': extract_customer_data()},
)

dbt_snap = BashOperator(
    task_id='dbt_snap',
    bash_command='dbt snapshot --project-dir /opt/airflow/transform --profiles-dir /opt/airflow/.dbt',
    dag=dag,
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run  --project-dir /opt/airflow/transform --profiles-dir /opt/airflow/.dbt',
    dag=dag,
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='dbt test --project-dir /opt/airflow/transform --profiles-dir /opt/airflow/.dbt',
    dag=dag,
)

end_of_ingestion = DummyOperator(task_id="end_of_ingestion", dag=dag)

(
    [
        extract_load_order_data,
        extract_load_customer_data,
    ]
    >> end_of_ingestion
    >> dbt_snap
    >> dbt_run
    >> dbt_test
)
