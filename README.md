# ✈️ Real-time Flight Data ETL & Analytics Pipeline

An end-to-end Data Engineering pipeline extracting live flight telemetry over Portugal from the OpenSky Network API, storing raw datasets in AWS S3 (Parquet), and transforming data into Silver and Gold analytical layers using **dbt** and **DuckDB**.

---

## 🏗️ Architecture & Medallion Design

The platform follows the **Medallion Architecture** to ensure data quality, explicit schema enforcement, and clear data lineage:

```text
                  ┌───────────────────────┐
                  │  OpenSky Network API  │
                  └───────────┬───────────┘
                              │ (Python Ingestion)
                              ▼
┌──────────────────────────────────────────────────────────┐
│ BRONZE LAYER: AWS S3 Data Lake                           │
│ Raw flight telemetry stored in Snappy-compressed Parquet │
└─────────────────────────────┬────────────────────────────┘
                              │ (dbt + DuckDB S3 Adapter)
                              ▼
┌──────────────────────────────────────────────────────────┐
│ SILVER LAYER: stg_flights (dbt View)                     │
│ Explicit type casting, data cleaning, timestamp handling │
└─────────────────────────────┬────────────────────────────┘
                              │ (dbt ref lineage)
                              ▼
┌──────────────────────────────────────────────────────────┐
│ GOLD LAYER: fct_flights_by_country (dbt View)            │
│ Business metrics: active aircrafts & flights by country  │
└──────────────────────────────────────────────────────────┘    
```

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Storage / Data Lake:** AWS S3 (Parquet format)
- **Transformations & Analytics Engineering:** dbt (dbt-core & dbt-duckdb)
- **Query Engine:** DuckDB (In-memory OLAP reading directly from S3)
- **Data Quality & Governance:** dbt tests (`not_null`, schema constraints)
- **Version Control:** Git & GitHub

---

## 📊 Data Models

### 1. Silver Layer (`stg_flights`)
- Cleans and casts 18 raw telemetry columns (e.g., `icao24`, `callsign`, `latitude`, `longitude`, `velocity`, `baro_altitude`).
- Normalizes timestamps from Unix epoch to standard datetime objects.

### 2. Gold Layer (`fct_flights_by_country`)
- Aggregates key flight metrics grouped by origin country:
  - `total_aircrafts`: Unique transponder IDs (`icao24`).
  - `total_flights`: Total active callsign records.
  - `avg_velocity_m_s`: Average flight speed in meters/second.
  - `avg_altitude_meters`: Average barometric altitude in meters.

---

## 🧪 Data Quality Tests

Data integrity is tested using dbt generic data tests defined in `analytics/models/schema.yml`:
- `stg_flights.icao24`: Checked for `not_null` constraints.
- `fct_flights_by_country.origin_country`: Checked for `not_null` constraints.

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.11+
- AWS credentials with read/write access to an S3 bucket

### 1. Clone & Setup Environment
git clone https://github.com/lucasFavieri/flight-etl-pipeline.git
cd flight-etl-pipeline

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

### 2. Configure Environment Variables
Create a .env file in the root directory:
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_aws_region
AWS_BUCKET_NAME=your_s3_bucket_name

### 3. Run Ingestion Pipeline (Python -> AWS S3)
python main.py

### 4. Run Transformations & Quality Tests (dbt + DuckDB)
cd analytics
dbt run
dbt test