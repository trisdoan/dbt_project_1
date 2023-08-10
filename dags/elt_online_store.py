from datetime import datetime, timedelta

##Airflow import###
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from src.extract_data import extract_order_data,load_order_data,extract_customer_data,load_customer_data




#Config
DBT_PROJECT_DIR = Variable.get('DBT_PROJECT_DIR')

#DAG Definition
default_args = {
    "owner": "warehouse",
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
    max_active_runs = 1
)


extract_load_order_data = PythonOperator(
    dag=dag,
    task_id="extract_load_order_data",
    python_callable=load_order_data,
    op_kwargs = {
        'order_data': extract_order_data()
    }
)


extract_load_customer_data = PythonOperator(
    dag=dag,
    task_id="extract_load_customer_data",
    python_callable=load_customer_data,
    op_kwargs = {
        'customer_data': extract_customer_data()
    }
)


dbt_snap = BashOperator(
    task_id='dbt_snap',
    bash_command='dbt snapshot --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}',
    dag=dag
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}',
    dag=dag
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}',
    dag=dag
)




end_of_pipeline = DummyOperator(task_id = "end_of_pipeline", dag=dag)


(
    [
        extract_load_order_data,
        extract_load_customer_data,

    ]
    >> dbt_snap
    >> dbt_run
    >> dbt_test
    >> end_of_pipeline
)
