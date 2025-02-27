from datetime import datetime, timedelta
import requests
import json
from airflow import DAG
from airflow.operators.python import PythonOperator

# FastAPI endpoint URL (Ensure FastAPI is running)
FASTAPI_HOST = "http://127.0.0.1:9000"  # Updated to match your FastAPI run command
API_URL = f"{FASTAPI_HOST}/fetch-weather/"
VENUES_API_URL = f"{FASTAPI_HOST}/api/venues/"

# Define start and end dates (yesterday to today)
START_DATE = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
END_DATE = datetime.utcnow().strftime("%Y-%m-%d")

# Function to fetch all venues from FastAPI
def get_venues():
    try:
        response = requests.get(VENUES_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"Error fetching venues: {e}")

# Function to fetch and store weather data
def fetch_and_store_weather():
    venues = get_venues()
    if not venues:
        raise Exception("No venues found")

    for venue in venues:
        payload = {
            "venues_id": venue["id"],  # Ensure field matches schemas.py
            "start_date": START_DATE,
            "end_date": END_DATE
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print(f"✅ Weather data stored for venue: {venue['name']}")
        except requests.RequestException as e:
            print(f" Failed to store weather data for venue {venue['name']}: {e}")

# Define the Airflow DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 26),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "fetch_weather_dag",
    default_args=default_args,
    description="DAG to fetch and store weather data daily",
    schedule_interval="0 0 * * *",  # Corrected key name
    catchup=False,
)

fetch_weather_task = PythonOperator(
    task_id="fetch_and_store_weather",
    python_callable=fetch_and_store_weather,
    dag=dag,
)

fetch_weather_task

