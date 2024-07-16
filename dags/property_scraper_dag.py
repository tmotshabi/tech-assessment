from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests, os
import pytz

flask_endpoint = os.environ.get('SITE_URL')
local_tz = pytz.timezone('Africa/Johannesburg')

default_args = {
    'owner': 'tshiamo',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def trigger_full_title_property_fetch():
    response = requests.post(f'{flask_endpoint}/get_full_title_property')
    print(response.text)

def trigger_sectional_title_property_fetch():
    response = requests.post(f'{flask_endpoint}/get_sectional_title_property')
    print(response.text)

with DAG(
    'fetch_properties_dag',
    start_date=datetime(2022, 1, 1, tzinfo=local_tz),
    default_args=default_args,
    description='DAG to fetch property data',
    schedule_interval='0 0 * * *',
    catchup=False,
) as dag:

    start_process = EmptyOperator(task_id='start_process', dag=dag)

    fetch_full_title_property = PythonOperator(
        task_id='fetch_full_title_property',
        python_callable=trigger_full_title_property_fetch,
        provide_context=True,
        dag=dag,
    )

    fetch_sectional_title_property = PythonOperator(
        task_id='fetch_sectional_title_property',
        python_callable=trigger_sectional_title_property_fetch,
        provide_context=True,
        dag=dag,
    )

    start_process >> fetch_full_title_property >> fetch_sectional_title_property
