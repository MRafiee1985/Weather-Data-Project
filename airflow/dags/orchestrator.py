from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from docker.types import Mount
from airflow.providers.docker.operators.docker import DockerOperator 
import sys

# Add path to import custom modules from api_request folder
sys.path.append('/opt/airflow')

# Import your ETL functions from insert_records
from api_request.get_api import connect_to_db, fetch_data
from api_request.insert_records import  main   


def run_insert_records():
    main(use_mock=False)  # Set to False for production use


default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2025, 7, 31),
    'catchup': False
}

# Define the DAG
with DAG(
    
    dag_id='weather_api_orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5)
) as dag:

    # Task 1: Fetch from API, recreate table, insert data
    fetch_and_insert = PythonOperator(
        task_id='fetch_and_insert_weather_data',
        python_callable=lambda: main(use_mock=False)
    )

    # Task 2: Transform using dbt inside Docker
    transform_weather_data = DockerOperator(
        task_id='transform_weather_data',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command=['run'],
        working_dir='/usr/app',
        mounts=[
            Mount(
                source='/home/marjan/repos/weather_data_project/dbt/my_project',
                target='/usr/app',
                type='bind'
            ),
            Mount(
                source='/home/marjan/repos/weather_data_project/dbt/profiles.yml',
                target='/root/.dbt/profiles.yml',
                type='bind'
            ),
            Mount(
                source='/var/run/docker.sock',
                target='/var/run/docker.sock',
                type='bind'
            ),
        ],
        network_mode='pg_network',
        docker_url='unix://var/run/docker.sock',
        auto_remove= 'success', 
        mount_tmp_dir=False
    )

    # Define task order
    fetch_and_insert >> transform_weather_data