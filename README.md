# ⚡ European Energy Grid & Pricing Engine

An end-to-end Modern Data Stack (MDS) pipeline built to extract, load, and transform live European weather conditions and energy market pricing. This project demonstrates a fully automated ELT architecture using Infrastructure as Code (IaC), cloud data warehousing, and dbt modeling.

## 🏗️ Architecture Overview

The pipeline operates on an hourly schedule to correlate weather patterns (temperature, windspeed) with the live Awattar energy market prices in Germany.

1. **Orchestration:** Apache Airflow (running locally via WSL)
2. **Extraction:** Python (`requests` library with header spoofing to bypass enterprise firewalls)
3. **Data Lake:** AWS S3 (Raw JSON landing zone)
4. **Data Warehouse:** Snowflake (Secure ingestion via AWS IAM Storage Integration)
5. **Transformation:** dbt Core (Medallion Architecture: Raw -> Staging -> Mart)
6. **Infrastructure as Code:** Terraform (AWS S3 & IAM provisioning)

## 📂 Project Structure

```text
lstoric-energy-engine/
├── dags/
│   └── energy_pipeline.py       # Master Airflow DAG (Extract -> Load -> Transform)
├── terraform/
│   └── main.tf                  # AWS S3 and IAM Role infrastructure
├── lstoric_transform/           # dbt Core Project
│   ├── models/
│   │   ├── stg_weather.sql      # Silver layer: Flattens Open-Meteo JSON
│   │   ├── stg_pricing.sql      # Silver layer: Flattens Awattar JSON
│   │   └── mart_energy_weather.sql # Gold layer: Joins weather & pricing on extraction hour
│   └── macros/
│       └── load_s3.sql          # Triggers Snowflake COPY INTO commands
└── README.md

Key Engineering Highlights
Corporate Network Bypass: Overcame standard urllib 502 Bad Gateway blocks by implementing requests with disguised Chrome User-Agent headers.

Secure Cloud Ingestion: Avoided hardcoded IAM keys by building a keyless Snowflake Storage Integration utilizing AWS IAM Roles and Trust Policies.

Schema-on-Read JSON Parsing: Utilized Snowflake's VARIANT column type to ingest nested API responses, flattening arrays natively via dbt SQL models.

Unified Orchestration: Eliminated competing schedulers (Snowflake Tasks vs. Airflow) by wrapping Snowflake COPY INTO commands inside dbt macros, allowing Airflow's BashOperator to natively orchestrate the entire ELT chain.

⚙️ Setup & Execution
Deploy AWS infrastructure using Terraform: cd terraform && terraform init && terraform apply

Configure Snowflake Storage Integration using the generated AWS Role ARN.

Start the local Airflow server: AIRFLOW_HOME=~/lstoric-energy-engine airflow standalone

Unpause the european_energy_extraction DAG in the Airflow UI to begin hourly ingestion.
