# ⚡ European Energy Grid & Pricing Engine

An end-to-end Modern Data Stack (MDS) pipeline built to extract, load, and transform live European weather conditions and energy market pricing. This project demonstrates a "Dual-Engine" architecture, utilizing both a Cloud Data Warehouse (Snowflake) for structured analytics and a Data Lakehouse (Databricks) for predictive modeling.

## 🏗️ Architecture Overview

The pipeline operates on an hourly schedule to correlate weather patterns (temperature, windspeed) with the live Awattar energy market prices in Germany.

1. **Orchestration:** Apache Airflow (running locally via WSL)
2. **Extraction:** Python (`requests` library with header spoofing to bypass enterprise firewalls)
3. **Data Lake:** AWS S3 (Raw JSON landing zone)
4. **Data Warehouse (Engine 1):** Snowflake (Secure ingestion via AWS IAM Storage Integration)
5. **Transformation:** dbt Core (Medallion Architecture: Raw -> Staging -> Mart)
6. **Data Lakehouse & ML (Engine 2):** Databricks Serverless (PySpark schema-on-read & predictive price volatility analysis)
7. **Infrastructure as Code:** Terraform (AWS S3 & IAM provisioning)

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
│   │   └── mart_energy_weather.sql # Gold layer: Joins weather & pricing
│   └── macros/
│       └── load_s3.sql          # Triggers Snowflake COPY INTO commands
├── Energy_Price_Predictor.ipynb # Databricks PySpark & ML Volatility Notebook
└── README.md
```
# Key Engineering Highlights
Dual-Engine Analytics: Engineered a hybrid data platform utilizing Snowflake/dbt for batch financial reporting and Databricks/PySpark for unstructured Big Data processing and Machine Learning preparation.

Serverless Egress Bypass: Overcame strict Databricks Free Edition network egress firewalls (which block standard Boto3 API calls) by routing raw JSON data through Databricks Volumes for localized PySpark ingestion.

Corporate Network Bypass: Overcame standard urllib 502 Bad Gateway blocks by implementing requests with disguised Chrome User-Agent headers.

Secure Cloud Ingestion: Avoided hardcoded IAM keys by building a keyless Snowflake Storage Integration utilizing AWS IAM Roles and Trust Policies.

Unified Orchestration: Eliminated competing schedulers by wrapping Snowflake COPY INTO commands inside dbt macros, allowing Airflow's BashOperator to natively orchestrate the entire ELT chain.

# Setup & Execution
Deploy AWS infrastructure using Terraform: cd terraform && terraform init && terraform apply

Configure Snowflake Storage Integration using the generated AWS Role ARN.

Start the local Airflow server: AIRFLOW_HOME=~/lstoric-energy-engine airflow standalone

Unpause the european_energy_extraction DAG in the Airflow UI to begin hourly ingestion.

(Optional) Import Energy_Price_Predictor.ipynb into Databricks to visualize market volatility.
