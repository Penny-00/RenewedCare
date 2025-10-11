# 🧠 RenewedCare Data Pipeline

> **RenewedCare** is a health data platform designed to support evidence-based decision-making across Nigeria’s Primary Health Care (PHC) system.  
> This repository hosts the **ETL (Extract, Transform, Load)** pipeline that automates ingestion of WHO and national health indicator datasets (e.g., Tuberculosis, Cholera, Mortality) into a PostgreSQL database.

---

## 📁 Project Overview

**Core Components**

- **FastAPI + SQLAlchemy ORM** – defines models and database connections
- **Alembic** – manages database schema migrations
- **ETL Pipeline** – Python scripts that load, clean, and insert CSV data into Postgres
- **PostgreSQL Database** – persistent storage layer for analytical queries and modeling

This project is designed for:

- **Data Engineers** – ETL and database maintenance
- **Data Scientists** – data exploration and model input preparation
- **Data Analysts** – dashboarding and reporting
- **Data Managers** – data validation and audits
- **AI Engineers** – training models on structured health data

---

## ⚡ Quick Start (for Non-Technical Users)

If you only want to **load or refresh data** (without writing any code):

1. Make sure PostgreSQL is running on your computer.
2. Open your terminal or command prompt inside the project folder (`renewedcare/`).
3. Run the command below:

## 🗂️ Project Structure

```bash
renewedCare-data-pipeline/
│
├── etl/
│   ├── load_disease_indicator.py
│   ├── load_mortality_data.py
│   ├── load_outbreak_reports.py
│   ├── load_all.py
│   └── __init__.py
│
├── data/processed
│   └─ processed/
│       ├─ disease_indicators/
│        ├─ tuberculosis_indicators_nga.csv
│        └─ malaria_indicators_nga.csv
│       ├─ mortality/
│        ├─ WHO_TOP_CAUSES_OF_DEATH_BOTH_GENDERS.csv
│        ├─ WHO_TOP_CAUSES_OF_DEATH_MALE.csv
│        └─ WHO_TOP_CAUSES_OF_DEATH_FEMALE.csv
│       └─ outbreaks/
│         ├─ cholera_adm0_public.csv
│         └─ ebola_adm0_public.csv
│
├── tests/
│   └── db_test.py         # Test database connection and table setup
│
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation (this file)
```

## ⚙️ Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.11+

- PostgreSQL (running locally or remotely)

- Git (for cloning the repo)

- pip (Python package manager)

- Virtual environment tool (optional but recommended)

## 🚀 Getting Started

### Clone the Repository

```bash
git clone  https://github.com/Penny-00/RenewedCare.git

cd renewedcare-data-pipeline
```

### Set Up a Virtual Environment

> 💡 Recommended to isolate project dependencies.

```bash
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows

```

### Install Dependencies

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

### Create .env in repo root (example):

```sql
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=RenewedCare
```

### Configure Database Connection

> Create a .env file in the project root and add your database credentials:

```bash
DATABASE_URL=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>
```

> Example:

```bash

DATABASE_URL=postgresql+psycopg2://postgres:admin@localhost:5432/renewedcare_db
```

## Alembic (migrations) — configuration & use

We recommend Alembic for schema management. Alembic should be installed via _requirements.txt_.

### Recommended migrations/env.py adjustments

Make sure migrations/env.py sets target_metadata from your app Base and uses the project DATABASE_URL. Example snippet to include early in env.py:

```python
import os, sys
sys.path.append(os.path.join(os.path.dirname(**file**), '..')) # make `app` importable

from app.database.db_connection import Base, DATABASE_URL # your db module

# IMPORTANT: import your model modules so their classes register on Base.metadata

from app.models import disease, disease_indicator, cause_of_death, mortality_statistic, outbreak_report

# Tell Alembic

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```

> If Alembic complains "Can't proceed with --autogenerate ... does not provide a MetaData object", it means target_metadata is missing or your model modules weren't imported.

### Typical commands

- Generate migration (autogenerate):

```bash
alembic revision --autogenerate -m "create initial tables"
```

- Apply migrations:

```bash
alembic upgrade head
```

- Stamp DB as current (if you manually align migrations):

```bash
alembic stamp head
```

If you ever remove a migration file but the DB still references it, you can clear **alembic_version** or use **alembic stamp** (see troubleshooting).

## 🧩 Running the ETL Pipeline

### Option A — Full Pipeline (Recommended for Engineers)

Run the full ETL pipeline (extract, transform, and load):

```bash

python -m etl.load_all
```

**This will:**

- Read and clean all CSV files in the /data directory

- Automatically create or rebuild tables in PostgreSQL

- Insert cleaned data into the database

- Logs will be printed to the console for tracking each step.

### Option B — Run a Specific ETL Component

If you only want to load a specific dataset (e.g., cholera):

```bash

python -m etl.load_outbreak_reports
```

> Or, for tuberculosis data:

```bash

python -m etl.load_tuberculosis_data
```

> Or WHO mortality data:

```bash

python -m etl.load_who_mortality
```

### Option C — For Data Scientists / Analysts

Once data is loaded, you can query it directly from the database using Python, Jupyter, or SQL tools.

> Example with Python:

```python

import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/renewedcare_db")
df = pd.read_sql("SELECT \* FROM cholera_reports", engine)
print(df.head())

```

## 🧑‍💻 Developer Notes

### For Data Engineers:

- Modify schemas dynamically in etl/load.py or etl/transform.py.

- Schema inference is handled automatically from CSV headers.

- If the database already exists, running the ETL again will not duplicate data — it checks for existing records before insert (you can adjust logic as needed).

### For Data Scientists:

- Use the loaded data for exploratory analysis or modeling.

- Cleaned data tables follow consistent naming and date formats.

### For Data Analysts:

- Connect BI tools (e.g., Power BI, Tableau, Metabase) to the PostgreSQL instance.

- You can also export queried data to CSV:

```python

df.to_csv("cholera_cleaned.csv", index=False)
```

### For Data Managers:

- Monitor logs for data updates.

- Check database schemas and record counts for consistency.

- Schedule automated ETL runs with cron or Airflow (future integration).

### 🤖 For AI Engineers

- The cleaned and normalized datasets can feed directly into AI pipelines for:

- Disease outbreak prediction

- Resource optimization modeling

- Patient triage support systems

- Consider building a feature store from these datasets for machine learning workflows.

## 💡 Non-Technical Users (Simple Data Load)

If you don’t want to touch any code, use this auto-load script:

1. Double-click the file named:

```bash
run_data_load.bat
```

(Windows)
or

```bash
run_data_load.sh
```

(Mac/Linux)

The script will:

- Activate the virtual environment

- Install dependencies (if not installed)

- Load all data automatically into PostgreSQL

- You’ll see progress messages in your terminal window.

> 🟢 No coding needed!
> Just ensure PostgreSQL is running and your .env file has the correct credentials.

## 🧪 Testing the Setup

Verify the connection to your database:

```bash

python -m tests.db_test
```

You should see:

```sql

INFO sqlalchemy.engine.Engine select pg_catalog.version()
✅ Database connection successful!
```

## 🧹 Rebuilding or Resetting the Database

If you want to delete and rebuild the database (start fresh):

```sql

DROP DATABASE renewedcare_db;
CREATE DATABASE renewedcare_db;
```

Then re-run the full ETL:

```bash

python -m etl.load_all
```

## 🧱 Future Improvements

- Add Airflow DAG for scheduled runs

- Integrate DBT for data transformation modeling

- Add data validation tests (e.g., Great Expectations)

- Include visualization dashboard (Metabase / Streamlit)

## 🏁 Conclusion

This project enables seamless collaboration across technical and non-technical teams.
From ETL developers to AI engineers — everyone can extract insights from reliable, clean, and up-to-date health data.
