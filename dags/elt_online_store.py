import json
from datetime import datetime, timedelta

##Airflow import###
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator

from src.extract_data import extract_order_data,load_order_data,extract_customer_data,load_customer_data

#DAG Definition
default_args = {
    "owner": "warehouse",
    "depends_on_past": True,
    "wait_for_downstream": True,
    "start_date": datetime(2023, 8, 4),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}
dag = DAG(
    "elt_online_store",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    max_active_runs = 1
)


extract_order_data_from_s3 = PythonOperator(
    dag=dag,
    task_id="extract_order_data",
    python_callable=extract_order_data
)

load_order_data_to_warehouse = PythonOperator(
    dag=dag,
    task_id="load_order_data_to_warehouse",
    python_callable=load_order_data
)


extract_customer_data_db = PythonOperator(
    dag=dag,
    task_id="extract_customer_data",
    python_callable=extract_customer_data
)

load_customer_data_to_warehouse = PythonOperator(
    dag=dag,
    task_id="load_customer_data_to_warehouse",
    python_callable=load_customer_data
)


end_of_pipeline = DummyOperator(task_id = "end_of_pipeline", dag=dag)

(
    extract_order_data
    >> load_order_data_to_warehouse
)

(
    extract_customer_data
    >> load_customer_data_to_warehouse
)

(
    [
        load_order_data_to_warehouse,
        load_customer_data_to_warehouse
    ]
    >> end_of_pipeline
)