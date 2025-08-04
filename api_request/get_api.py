import requests
import logging
import psycopg2
import os
import json



# api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York" 


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="db",              # from POSTGRES_DB
            user="db_user",           # from POSTGRES_USER
            password="db_password",   # from POSTGRES_PASSWORD
            host= "db",              # from docker-compose service name
            port="5432"
        )   
        print(f"✅ Successfully connected to database")  
        return conn

    except psycopg2.OperationalError as e:
        raise RuntimeError(f"❌ Could not connect to PostgreSQL: {e}") 



def fetch_data():
    WEATHERSTACK_KEY="ab807c806cc7c9d02bb423de92820f1f"
    api_key = os.environ.get("WEATHERSTACK_KEY", WEATHERSTACK_KEY) 
    if not api_key:
        raise RuntimeError("WEATHERSTACK_KEY is not set in environment")

    url = "http://api.weatherstack.com/current"
    params = {
        "access_key": api_key,
        "query":      "New York"  
    }

    print("Fetching data from the weather API...")
    response = requests.get(url, params=params)
    response.raise_for_status()
    print("Request was successful!")
    return response.json()


def mock_fetch_data():
    return  {'request': {'type': 'City', 'query': 'New York, United States of America','language': 'en', 'unit': 'm'}, 
            'location': {'name': 'New York', 'country': 'United States of America','region': 'New York', 'lat': '40.714', 'lon': '-74.006', 
            'timezone_id': 'America/New_York','localtime': '2025-07-21 23:37', 'localtime_epoch': 1753141020, 'utc_offset': '-4.0'}, 
            'current': {'observation_time': '03:37 AM', 'temperature': 24, 'weather_code': 113, 
            'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0008_clear_sky_night.png'], 
            'weather_descriptions': ['Clear '], 'astro': {'sunrise': '05:43 AM', 'sunset': '08:21 PM', 'moonrise': '01:53 AM', 
            'moonset': '06:07 PM', 'moon_phase': 'Waning Crescent', 'moon_illumination': 18}, 
            'air_quality': {'co': '344.1', 'no2': '25.53', 'o3': '41', 'so2': '6.105', 'pm2_5': '9.435', 'pm10': '9.435', 'us-epa-index': '1', 'gb-defra-index': '1'},
            'wind_speed': 16, 'wind_degree': 13, 'wind_dir': 'NNE', 'pressure': 1017, 'precip': 0, 'humidity': 40, 'cloudcover': 0, 
            'feelslike': 26, 'uv_index': 0, 'visibility': 16, 'is_day': 'no'}}




if __name__ == "__main__":
    conn = connect_to_db()
    data = fetch_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    conn.close()
    print("🔒 Database connection closed.")
