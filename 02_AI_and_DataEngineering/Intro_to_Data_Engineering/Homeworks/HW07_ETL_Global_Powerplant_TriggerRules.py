# ETL for Global Powerplant with validation by trigger rules

from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context
from airflow.utils.trigger_rule import TriggerRule
from airflow.exceptions import AirflowSkipException
from datetime import datetime, timedelta, timezone
import pandas as pd
import sqlite3, os

# Setting up the Paths

DATA_PATH = '/home/eddierednic/airflow/datasets/global_power_plant_database.csv'
DB_PATH = '/home/eddierednic/airflow/databases/power_plant.db'
EXTRACTED_PATH = '/tmp/gppd_extracted.csv'
TRANSFORMED_PATH = '/tmp/gppd_transformed.csv'

# Here we do our DAG configuration

default_args = {
    'owner': 'eddierednic',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'gppd_etl_min2',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Simple ETL for Global Power Plant data with validation by using trigger rules',
)

CRITICAL = ['capacity_mw', 'commissioning_year']

# 1) Extract: reading the CSV, writing a temporary copy and pushing the path

def extract():
    df = pd.read_csv(DATA_PATH)
    df.to_csv(EXTRACTED_PATH, index=False)
    get_current_context()['ti'].xcom_push(key='extracted_path', value=EXTRACTED_PATH)

extract_task = PythonOperator(
    task_id='extract_task',
    python_callable=extract,
    dag=dag
    )

# 2) Transform: filling the NAs and adding age_of_plant, also pushing the new path

def transform():
    ti = get_current_context()['ti']
    src = ti.xcom_pull(task_ids='extract_task', key='extracted_path')
    df = pd.read_csv(src)

    # Making sure the critical columnss exist

    for c in CRITICAL:
        if c not in df.columns:
            df[c] = None

    # Here we do our numberic and median fill

    df['capacity_mw'] = pd.to_numeric(df['capacity_mw'], errors='coerce')
    df['commissioning_year'] = pd.to_numeric(df['commissioning_year'], errors='coerce')
    df['capacity_mw'] = df['capacity_mw'].fillna(df['capacity_mw'].median())
    year_median = df['commissioning_year'].median() if df['commissioning_year'].notna().any() else datetime.now(timezone.utc).year
    df['commissioning_year'] = df['commissioning_year'].fillna(year_median)

    # Here we have our new columns

    now_year = datetime.now(timezone.utc).year
    df['age_of_plant'] = (now_year - df['commissioning_year']).clip(lower=0)

    df.to_csv(TRANSFORMED_PATH, index=False)
    ti.xcom_push(key='transformed_path', value=TRANSFORMED_PATH)

transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform,
    dag=dag
    )

# 3) Validate: if still missing -> skip load

def validate():
    ti = get_current_context()['ti']
    path = ti.xcom_pull(task_ids='transform_task', key='transformed_path')
    df = pd.read_csv(path)

    for c in CRITICAL:
        if df[c].isna().any():
            # makes downstream (with all_success) not run
            raise AirflowSkipException(f'Validation failed: {c} still missing.')

validate_task = PythonOperator(task_id='validate_task', python_callable=validate, dag=dag)

# 4) Load: creating the table (but its good practise I guess to use if not exists) and inserting rows

def load():
    ti = get_current_context()['ti']
    path = ti.xcom_pull(task_ids='transform_task', key='transformed_path')
    df = pd.read_csv(path)

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS power_plant_data (
        country TEXT, country_long TEXT, name TEXT, gppd_idnr TEXT, capacity_mw REAL,
        latitude REAL, longitude REAL, primary_fuel TEXT, other_fuel1 TEXT, other_fuel2 TEXT, other_fuel3 TEXT,
        commissioning_year REAL, owner TEXT, source TEXT, url TEXT, geolocation_source TEXT, wepp_id TEXT,
        year_of_capacity_data REAL, generation_gwh_2013 REAL, generation_gwh_2014 REAL, generation_gwh_2015 REAL,
        generation_gwh_2016 REAL, generation_gwh_2017 REAL, generation_gwh_2018 REAL, generation_gwh_2019 REAL,
        generation_data_source TEXT, estimated_generation_gwh_2013 REAL, estimated_generation_gwh_2014 REAL,
        estimated_generation_gwh_2015 REAL, estimated_generation_gwh_2016 REAL, estimated_generation_gwh_2017 REAL,
        estimated_generation_note_2013 TEXT, estimated_generation_note_2014 TEXT, estimated_generation_note_2015 TEXT,
        estimated_generation_note_2016 TEXT, estimated_generation_note_2017 TEXT, age_of_plant REAL
    );
    """)

    # Organising the columns, changing missing to None (Had some help here on this part)

    needed = [c[1] for c in cur.execute("PRAGMA table_info(power_plant_data);").fetchall()]
    for col in needed:
        if col not in df.columns:
            df[col] = None
    df = df[needed].where(df.notna(), None)

    df.to_sql('power_plant_data', conn, if_exists='append', index=False)
    conn.commit(); conn.close()

load_task = PythonOperator(
    task_id='load_task',
    python_callable=load, 
    dag=dag
    )

# Our trigger rule (default is set to all_success, I set it so it’s visible, not sure if that's the right way)

load_task.trigger_rule = TriggerRule.ALL_SUCCESS

# Order is: Extract -> Transform -> Validate -> Load

extract_task >> transform_task >> validate_task >> load_task
