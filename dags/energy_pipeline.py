from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import requests
import json
import boto3
import time

# --- CONFIGURATION ---
S3_BUCKET = "smart-meter-raw-data-luka-frankfurt" 
# ---------------------

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"}

def extract_weather_data():
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.1109&longitude=8.6821&current_weather=true"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    s3 = boto3.client('s3')
    unique_id = int(time.time())
    file_name = f"raw_data/weather/weather_frankfurt_{unique_id}.json"
    s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=json.dumps(response.json()))
    print(f"Weather data saved to S3")

def extract_energy_price():
    url = "https://api.awattar.de/v1/marketdata"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    s3 = boto3.client('s3')
    unique_id = int(time.time())
    file_name = f"raw_data/pricing/awattar_germany_{unique_id}.json"
    s3.put_object(Bucket=S3_BUCKET, Key=file_name, Body=json.dumps(response.json()))
    print(f"Pricing data saved to S3")

default_args = {
    'owner': 'lstoric',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'european_energy_extraction',
    default_args=default_args,
    description='Master End-to-End ELT Pipeline',
    schedule=timedelta(hours=1),
    catchup=False
) as dag:

    # 1. EXTRACT 
    fetch_weather = PythonOperator(task_id='extract_live_weather', python_callable=extract_weather_data)
    fetch_price = PythonOperator(task_id='extract_energy_price', python_callable=extract_energy_price)

    # 2. LOAD 
    load_to_snowflake = BashOperator(
        task_id='load_s3_to_snowflake',
        bash_command='cd ~/lstoric-energy-engine/lstoric_transform && dbt run-operation load_s3_data'
    )

    # 3. TRANSFORM 
    transform_data = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd ~/lstoric-energy-engine/lstoric_transform && dbt run'
    )

    # THE ORCHESTRATION GRAPH
    [fetch_weather, fetch_price] >> load_to_snowflake >> transform_data

