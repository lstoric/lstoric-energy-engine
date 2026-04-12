# European Energy Grid & Pricing Engine

An end-to-end Modern Data Stack (MDS) pipeline built to extract, load, and transform live European weather conditions and energy market pricing. This project demonstrates a "Dual-Engine" architecture utilizing a Cloud Data Warehouse (Snowflake) and a Data Lakehouse (Databricks), complete with automated CI/CD and an interactive BI dashboard.

## Architecture Overview

The pipeline operates on an hourly schedule to correlate weather patterns (temperature, windspeed) with the live Awattar energy market prices in Germany.

1. **Infrastructure as Code:** Terraform (AWS S3 & IAM provisioning)
2. **Orchestration:** Apache Airflow (running locally via WSL)
3. **Extraction:** Python (`requests` library with header spoofing to bypass enterprise firewalls)
4. **Data Lake:** AWS S3 (Raw JSON landing zone)
5. **Data Warehouse:** Snowflake (Secure ingestion via AWS IAM Storage Integration)
6. **Transformation:** dbt Core (Medallion Architecture: Raw -> Staging -> Mart)
7. **Business Intelligence:** Streamlit (Interactive web dashboard visualizing Snowflake Gold Layer data)
8. **Data Lakehouse / ML:** Databricks Serverless (PySpark schema-on-read & predictive analytics)
9. **CI/CD Automation:** GitHub Actions (Automated Python linting and DAG code-quality checks)

## Project Structure

```text
lstoric-energy-engine/
├── .github/workflows/
│   └── data_pipeline_ci.yml     # CI/CD Pipeline (GitHub Actions)
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
├── dashboard.py                 # Streamlit BI Web Application
├── Energy_Price_Predictor.ipynb # Databricks PySpark & ML Volatility Notebook
└── README.md
```

## Key Engineering Highlights

* **Automated CI/CD Pipelines:** Implemented GitHub Actions to automatically run `flake8` syntax and complexity checks on all Apache Airflow DAGs prior to merging, ensuring pipeline stability.
* **Interactive Business Intelligence:** Engineered a Streamlit web application to serve as the presentation layer, allowing business stakeholders to easily interact with market volatility metrics derived from the Snowflake Gold Layer.
* **Dual-Engine Analytics:** Engineered a hybrid data platform utilizing Snowflake/dbt for batch financial reporting and Databricks/PySpark for unstructured Big Data processing.
* **Serverless Egress Bypass:** Overcame strict Databricks network egress firewalls by routing raw JSON data through Databricks Volumes for localized PySpark ingestion.
* **Corporate Network Bypass:** Overcame standard `urllib` 502 Bad Gateway blocks by implementing `requests` with disguised Chrome User-Agent headers.
* **Secure Cloud Ingestion:** Avoided hardcoded IAM keys by building a keyless Snowflake Storage Integration utilizing AWS IAM Roles and Trust Policies.

## Setup and Execution

1. Deploy AWS infrastructure: `cd terraform && terraform init && terraform apply`
2. Start the local Airflow server: `source airflow-venv/bin/activate && AIRFLOW_HOME=~/lstoric-energy-engine airflow standalone`
3. Launch the BI Dashboard: `source airflow-venv/bin/activate && streamlit run dashboard.py`

## Author
Luka Storic, *Data Engineer*
