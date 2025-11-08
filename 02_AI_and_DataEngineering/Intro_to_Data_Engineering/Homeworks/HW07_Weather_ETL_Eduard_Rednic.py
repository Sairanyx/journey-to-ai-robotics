from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context
from datetime import datetime, timedelta
import pandas as pd
import sqlite3


DATA_PATH = '/home/eddierednic/airflow/datasets/weather_data.csv'
DB_PATH = '/home/eddierednic/airflow/databases/weather_database.db'
EXTRACTED_PATH = '/tmp/extracted_weather.csv'
TRANSFORMED_PATH = '/tmp/transformed_weather.csv'

default_args = {
    'owner': 'eddierednic',
    'depends_on_past': False,
    'start_date': datetime(2025,10,28),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)

}

dag = DAG(
    'weatherdata_etl',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='SimpleETL pipeline for weather data to SQLite',

)

# Task 1: Extract data from csv

def extract_weather_data():
    df = pd.read_csv(DATA_PATH)
    df.to_csv(EXTRACTED_PATH, index=False)
    get_current_context()['ti'].xcom_push(key='extracted_path', value=EXTRACTED_PATH)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract_weather_data,
    dag=dag
)

# Task 2: Handle missing values and add median, calculate feels_like temp

def transform_data():
    ti = get_current_context()['ti']
    src = ti.xcom_pull(task_ids='extract_task', key='extracted_path')
    df = pd.read_csv(src)

    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')
    df['wind_speed'] = pd.to_numeric(df['wind_speed'], errors='coerce')

    df['temperature'].fillna(df['temperature'].median(), inplace=True)
    df['humidity'] = df['humidity'].fillna(0)
    df['wind_speed'] = df['wind_speed'].fillna(0)
    df['feels_like_temperature'] = df['temperature'] + 0.33*df['humidity'] - 0.7*df['wind_speed'] - 4

    df.to_csv(TRANSFORMED_PATH, index=False)
    ti.xcom_push(key='transformed_path', value=TRANSFORMED_PATH)

transform_task = PythonOperator(
    task_id = 'transform_task',
    python_callable=transform_data,
    dag=dag,
)

def load_data():
    ti = get_current_context()['ti']
    path = ti.xcom_pull(task_ids='transform_task', key='transformed_path')
    df = pd.read_csv(path)

    conn = sqlite3.connect(DB_PATH)

    df.to_sql('weather_data', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load_data,
    dag=dag
)

extract_task >> transform_task >> load_task