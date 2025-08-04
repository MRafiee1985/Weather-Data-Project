import logging
from psycopg2 import Error as psycopg2_Error
from api_request.get_api import fetch_data, mock_fetch_data, connect_to_db
import json
from datetime import datetime 

# -------------------------
# Configure Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------------
# Create (or Recreate) Table
# -------------------------
def create_table(conn):
    """
    Drop the old weather_data table (if any) and create a fresh one
    with the correct columns.
    """
    try:
        with conn.cursor() as cursor:
            # Kill any old table so our columns are always in sync
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS raw_weather_data (
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    temperature FLOAT,
                    weather_descriptions TEXT,
                    wind_speed FLOAT,
                    time_local TIMESTAMP,
                    utc_offset TEXT
                    );
              """)
        conn.commit()
        logging.info("✅ Table 'raw_weather_data' recreated with correct schema.")
    except psycopg2_Error as e:
        logging.error(f"❌ Failed to create table: {e}")
        raise

# -------------------------
# Insert Record
# -------------------------
def insert_records(conn, data):
    """
    Insert one record of weather data into raw_weather_data table.
    Maps JSON 'localtime' → DB 'local_time'.
    """
    try:
        location = data.get('location', {})
        current  = data.get('current', {})
        
        #  Required keys 
        required_keys_loc = ['name','country', 'localtime', 'utc_offset' ]
        required_keys_curr = ['temperature', 'weather_descriptions', 'wind_speed']
        missing = [k for k in required_keys_loc if k not in location] + \
                  [k for k in required_keys_curr if k not in current]
        if missing:
            raise ValueError(f"⚠️ Missing required keys: {missing}")

        city                 = location['name']
        utc_offset           = location['utc_offset']
        time_local           = location['localtime']                  
        temperature          = current['temperature']
        weather_descriptions = json.dumps(current['weather_descriptions'])   
        wind_speed           = current['wind_speed']
                  

        with conn.cursor() as cursor:
             cursor.execute("""
                INSERT INTO raw_weather_data
                  (city, temperature, weather_descriptions, wind_speed, time_local, utc_offset)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                city,
                temperature,
                weather_descriptions,
                wind_speed,
                time_local,
                utc_offset
            ))
        conn.commit()
        logging.info("✅ Weather data inserted successfully.")
    except psycopg2_Error as e:
        logging.error(f"❌ Database insertion error: {e}")
        raise
    except Exception as e:
        logging.error(f"❌ Unexpected error during insertion: {e}")
        raise

# -------------------------
# Main ETL Logic
# -------------------------
def main(use_mock: bool = False):
    """
    Fetch weather data, recreate table, then insert one row.
    """
    conn = None
    try:
        data =  fetch_data() if not use_mock else mock_fetch_data()
        # payload =  mock_fetch_data() if use_mock else fetch_data()
         

        conn = connect_to_db()
        create_table(conn)           # always drops & recreates
        insert_records(conn, data)
    except Exception as e:
        logging.error(f"❌ ETL process failed: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("🔒 Database connection closed.")

# -------------------------
# Script Entry Point
# -------------------------
if __name__ == "__main__":
    main(use_mock=False)  # Set to False for production use

