# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.providers.docker.operators.docker import DockerOperator 
# from datetime import datetime, timedelta
# from docker.types import Mount
# import sys
# import os 

# # Add path to import custom modules from api_request folder
# # sys.path.append('/opt/airflow')
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Import your ETL functions from insert_records
# # from api_request.get_api import connect_to_db, mock_fetch_data , fetch_data
# from api_request.insert_records import  main


# def run_main():
#     main(use_mock=False)  # Set to False for production use

# # Default arguments for DAG
# default_args = {
#     'description': 'A DAG to orchestrate data',
#     'start_date': datetime(2025, 7, 31),
#     'catchup': False
# }

# # Define the DAG
# dag = DAG(
#     dag_id='weather-dbt-orchestrator',
#     default_args=default_args,
#     schedule=timedelta(minutes=5)
# )

# # Define the task(s)
# with dag:

#     task1 = PythonOperator(
#         task_id='ingest_data_task',
#         python_callable=run_main 
#     )

#     task2 = DockerOperator(
#     task_id='transform_data_task',
#     image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
#     command='run',
#     working_dir='/usr/app',
#     mounts=[
#         Mount(
#             source= '/home/marjan/repos/weather_data_project/dbt/my_project',
#             target='/usr/app',
#             type='bind'
#         ),
#         Mount(
#             source='/home/marjan/repos/weather_data_project/dbt/profiles.yml',
#             target='/root/.dbt/profiles.yml',
#             type='bind'
#         ),
#         Mount(  
#             source='/var/run/docker.sock',
#             target='/var/run/docker.sock',
#             type='bind'
#     )
#     ],
#     network_mode='pg_network',
#     docker_url= "unix://var/run/docker.sock",
#     auto_remove='success',
#         )


#     # 🔗 Define execution order
#     task1 >> task2 

