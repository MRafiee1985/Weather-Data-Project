# Weather Data Project

## Project Description
The **Weather Data Project** demonstrates an end‑to‑end data engineering pipeline for ingesting, transforming, and visualizing weather information. The workflow:
1. Fetches weather data from a public API.
2. Loads the raw data into a PostgreSQL database.
3. Transforms the data using [dbt](https://www.getdbt.com/).
4. Explores and visualizes the transformed data in [Apache Superset](https://superset.apache.org/).
5. Orchestrates the entire process with [Apache Airflow](https://airflow.apache.org/).

## Project Structure
| Folder / File | Description |
|---------------|-------------|
| `airflow/`    | Airflow DAGs that orchestrate data ingestion and transformation. |
| `api_request/`| Python scripts to call the weather API and write data into PostgreSQL. |
| `dbt/`        | dbt project containing models, profiles, and transformation logic. |
| `docker/`     | Helper scripts and configuration for Superset and other services. |
| `postgres/`   | SQL initialization scripts for Airflow and Superset databases. |
| `tests/`      | Basic unit tests for API requests and ETL logic. |
| `docker-compose.yml` | Docker Compose definition for all services in the stack. |

## Prerequisites
Ensure the following tools are installed before starting:
- [Python 3.10+](https://www.python.org/)
- [Docker & Docker Compose](https://www.docker.com/)
- [dbt](https://docs.getdbt.com/docs/core/installation)
- [Apache Airflow](https://airflow.apache.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Apache Superset](https://superset.apache.org/)
- `git`

> **Tip:** Most dependencies are containerized via Docker. Local installations are mainly needed for development and testing.

## Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/Weather-Data-Project.git
   cd Weather-Data-Project
   ```
2. **Create the Docker network (if it doesn't exist)**
   ```bash
   docker network create pg_network
   ```
3. **Start all containers**
   ```bash
   docker compose up -d
   ```
   This launches PostgreSQL, Airflow, dbt, Superset, and Redis.
4. **Access Airflow**
   - UI: [http://localhost:8081](http://localhost:8081)
   - Default credentials: `airflow` / `airflow`
5. **Initialize dbt (optional for local runs)**
   ```bash
   cd dbt/my_project
   dbt deps
   ```
6. **Superset setup**
   - UI: [http://localhost:8088](http://localhost:8088)
   - Default credentials: `admin` / `admin`

## Running the Pipeline
1. Open the Airflow UI at `http://localhost:8081`.
2. Locate the DAG named **`weather_api_orchestrator`**.
3. Trigger the DAG manually or let it run on its 5‑minute schedule.
   - Task 1: fetches weather data and loads it into the `raw_weather_data` table.
   - Task 2: runs dbt models to transform the raw data.

## Viewing Results in Superset
1. Log in to Superset at `http://localhost:8088`.
2. In *Datasets*, connect to the PostgreSQL database and select the transformed weather tables.
3. Create charts and dashboards to explore the weather data.

## Technologies Used
- Python
- PostgreSQL
- dbt
- Apache Airflow
- Apache Superset
- Docker & Docker Compose

## Contact
**Author:** Marjan Rafiee  
**Email:** m.rafiee1985@gmail.com

---
Feel free to open issues or submit pull requests for improvements!
