# Real‑Time Weather Dashboard (Python · Airflow · Docker)

Build a **real‑time weather data pipeline** that ingests from an external API, lands raw data in PostgreSQL, transforms it with **dbt**, orchestrates everything with **Apache Airflow**, and visualizes insights in **Apache Superset**. This repository is designed as a practical, portfolio‑ready project showcasing end‑to‑end data engineering on your local machine via Docker.

> ⚠️ This README assumes Docker Desktop is installed and you’re comfortable running commands in a terminal/WSL. Replace any placeholder values (like `YOUR_*`) with your own.

---

## ✨ Features

- **API ingestion** of current weather for one or more cities (Weatherstack).
- **Reliable storage** in PostgreSQL with a clear `dev` schema and typed columns.
- **Incremental‑friendly modeling** in dbt:
  - `stg_weather_data` (staging) with timezone handling & de‑duplication.
  - Simple **marts** for reporting (daily averages, quick “weather report” table).
- **Orchestration** with Airflow (DAGs, task dependencies, Dockerized operator for dbt).
- **Dashboards** in Superset (auto‑refresh) to monitor temperature & wind patterns.
- **Secure configuration** via environment variables (.env) with secrets kept out of git.
- **Troubleshooting guide** for common Docker / networking / permissions issues.

---

## 🗺️ Architecture (high‑level)

```
Weatherstack API  -->  Airflow (Ingest Task) ---> PostgreSQL (raw/dev)
                                                │
                                                └---> dbt (staging + marts)
                                                        │
                                                        └---> Superset (dashboards)
```

> Suggested image: add `docs/architecture.png` to illustrate the above flow.

---

## 🧰 Tech Stack

- **Python 3** (requests, psycopg2)
- **Docker & Docker Compose**
- **PostgreSQL**
- **Apache Airflow**
- **dbt (Core)** for SQL‑first transformations
- **Apache Superset** for BI dashboards

---

## 📁 Repository Structure (suggested)

```
.
├─ docker-compose.yml
├─ .env.example
├─ airflow/
│  └─ dags/
│     └─ weather_pipeline.py             # Orchestrates ingestion + dbt
├─ dbt/
│  ├─ dbt_project.yml
│  └─ models/
│     ├─ sources/
│     │  └─ sources.yml                  # Declares raw table/columns
│     ├─ staging/
│     │  └─ stg_weather_data.sql         # Timezone, renames, de-dup
│     └─ marts/
│        ├─ weather_report.sql
│        └─ daily_average.sql
├─ app/
│  ├─ weather_api.py                     # API client
│  └─ db.py                              # Database helpers (connect/insert)
└─ superset/
   ├─ dockerinit.sh
   ├─ dockerbootstrap
   ├─ superset_config.py
   └─ .env
```

> File and folder names are illustrative—keep your actual paths consistent with your code and `docker-compose.yml`.

---

## 🔑 Environment Variables

Create a `.env` from the example and fill in values:

```bash
cp .env.example .env
```

Minimum variables you’ll likely need:

```dotenv
# Weather API
WEATHERSTACK_API_KEY=YOUR_WEATHERSTACK_API_KEY

# Postgres
POSTGRES_USER=YOUR_DB_USER
POSTGRES_PASSWORD=YOUR_DB_PASSWORD
POSTGRES_DB=YOUR_DB_NAME

# Optional: target cities, comma-separated (handled by your code/DAG)
CITIES=Toronto,Montreal
```

> Keep the `.env` file out of version control.

---

## 🚀 Getting Started

### 1) Clone & prepare Python (optional local venv)

```bash
python3 -m venv venv
source venv/bin/activate   # Windows/WSL: source venv/bin/activate
pip install -r requirements.txt
```

### 2) Start the stack

```bash
docker compose up -d --build
```

This should bring up:
- **PostgreSQL** (mapped to your local port defined in `docker-compose.yml`)
- **Airflow Webserver & Scheduler** (mapped web port)
- **Superset** (BI UI, mapped web port)
- Any helper containers (init, networks, etc.)

### 3) Initialize the database schema

Create the `dev` schema for raw/staging tables (adjust user/db to your `.env`):

```bash
docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "CREATE SCHEMA IF NOT EXISTS dev;"
```

### 4) First run: trigger the pipeline

- Open **Airflow UI** (the port you mapped in compose) and unpause/trigger the weather DAG.
- The ingestion task should fetch weather data and insert into PostgreSQL.
- The dbt task (via Dockerized operator or CLI) should build the staging and marts.

### 5) Explore the data

Using `psql`:

```bash
docker compose exec db psql -U $POSTGRES_USER -d $POSTGRES_DB

-- inside psql
\dn                       -- list schemas
SET search_path TO dev, public;
SELECT * FROM stg_weather_data LIMIT 10;
SELECT * FROM weather_report LIMIT 10;
SELECT * FROM daily_average LIMIT 10;
```

### 6) Visualize in Superset

- Open **Superset UI**, add a database connection to your PostgreSQL service.
- Create a dataset from `dev.stg_weather_data` or your marts.
- Build a dashboard and set an **auto‑refresh** interval (e.g., 5 minutes).

---

## 🧱 Data Model

**Raw/Staging Columns** (typical):
- `id` (serial PK)
- `city` (text)
- `temperature` (float)
- `weather_description` (text)
- `wind_speed` (float)
- `time_utc` (timestamp)
- `inserted_at` (timestamp default now)
- `utc_offset` (text)

**Key transformations** in `stg_weather_data.sql`:
- Rename time columns and **convert timestamps to local time**.
- Handle `utc_offset` and any API quirks.
- **De‑duplicate** with a window function (keep first record per time slice).

**Marts**
- `weather_report.sql`: select essential, user‑friendly columns.
- `daily_average.sql`: `AVG(temperature)`, `AVG(wind_speed)` grouped by `city` + `date` (rounded).

---

## ⏱️ Scheduling

- Default: frequent runs for development (e.g., every 1 minute) so you can validate end‑to‑end.
- For production‑like usage, consider **every 5 minutes** or higher to respect API limits.

> Remember most free weather APIs have rate limits—design for caching/minimal calls.

---

## 🔐 Security & Config Best Practices

- Use **environment variables** for secrets and connection strings.
- Regularly **update dependencies** and Docker images.
- Limit database user permissions to least‑privilege for services.
- Avoid committing any `.env` or credentials to git.

---

## 🛠️ Troubleshooting

- **Permission errors** (e.g., creating files inside containers): ensure correct `chown`/`chmod` on mounted volumes.
- **Import/module issues**: check container PYTHONPATH and installed packages.
- **Network problems**: verify the Docker network name, **service aliases**, and that services depend on each other correctly.
- **DB connection failures**: confirm ports, user/password, and that the DB service is healthy.
- **dbt in DockerOperator**: mount project and profiles, pass correct environment, and ensure the operator can reach the DB host (use service name, e.g., `db`).

Commands you may find handy:

```bash
docker compose logs -f <service>
docker compose exec <service> bash
docker compose down -v   # ❗ removes volumes; only for resetting local state
```

---

## 📈 Roadmap / Nice‑to‑Haves

- Add structured **logging & metrics** (task‑level + app logs).
- Implement **tests** (dbt tests, data freshness, Great Expectations).
- Switch to **incremental models** for staging/marts.
- Add **CI/CD** (linters, `dbt build`, basic pipeline tests on PR).
- Embed a ready‑made **Superset dashboard JSON** for quick import.

---

## 🙌 Acknowledgements

- Weather data via **Weatherstack**.
- BI and orchestration by the amazing open‑source projects **Apache Superset** and **Apache Airflow**.
- dbt Core for a clean, testable SQL‑first transformation layer.

---

## 📜 License

Choose a license for your repository (e.g., MIT) and add it as `LICENSE`.
