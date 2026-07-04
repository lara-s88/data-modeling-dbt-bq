# Data Modeling with dbt and BigQuery

![dbt CI Pipeline](https://github.com/lara-s88/data-modeling-dbt-bq/actions/workflows/dbt_ci.yml/badge.svg)

## Project Overview
End-to-end automated data pipeline using dbt and Google BigQuery to transform 
1.5M+ raw sales records into clean, tested, and analytics-ready models.
Built as part of the DEPI Data Engineering Program — Project 9.

## Architecture
Raw Data Generation
↓
Google BigQuery - Data Warehouse
raw_sales     (1,500,000 rows)
raw_customers (1,000 rows)
raw_products  (50 rows)
↓
dbt - Transformation Layer
Staging → cleans & types raw data (views)
Marts   → applies business logic (tables)
↓
BigQuery - Analytical Layer
fact_sales / dim_customer / dim_product
↓
Power BI - Dashboard Layer

## Tech Stack
| Tool | Version | Purpose |
|---|---|---|
| Google BigQuery | Sandbox | Cloud data warehouse |
| dbt Core | 1.11.11 | Data transformation & testing |
| Python | 3.11 | dbt runtime |
| GitHub Actions | - | CI/CD pipeline & scheduling |
| Power BI | Desktop | Business intelligence dashboard |

## Data Models

### Staging Layer
| Model | Source | Description |
|---|---|---|
| stg_sales | raw_sales | Cleaned sales transactions |
| stg_customers | raw_customers | Cleaned customer data |
| stg_products | raw_products | Cleaned product data |

### Marts Layer
| Model | Type | Description |
|---|---|---|
| fact_sales | Fact | Sales with revenue & profit calculations |
| dim_customer | Dimension | Customer attributes & segmentation |
| dim_product | Dimension | Product attributes & pricing |

## Data Quality
- **Total tests:** 47
- **Passed:** 47 ✅
- **Failed:** 0
- **Test types:** unique, not_null, accepted_values, relationships

## CI/CD Pipeline
Every push to `main` AND every day at midnight, GitHub Actions automatically:
1. Sets up Python 3.11
2. Installs dbt-bigquery
3. Authenticates to BigQuery
4. Runs `dbt run`
5. Runs `dbt test`
6. Reports ✅ or ❌ on GitHub

## Lineage Graph
raw_sales ──────→ stg_sales ──────→ fact_sales ──→ Power BI
raw_customers ──→ stg_customers ──→ dim_customer ↗
raw_products ───→ stg_products ───→ dim_product ─→ Power BI

## How to Run Locally

### Prerequisites
- Python 3.11+
- `bq-key.json` service account key (get from team lead privately)

### Setup
```bash
git clone https://github.com/lara-s88/data-modeling-dbt-bq.git
cd data-modeling-dbt-bq
python -m venv venv
venv\Scripts\activate.bat
pip install dbt-bigquery
```

```yaml
# C:\Users\YOUR_NAME\.dbt\profiles.yml
sales_analytics:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: bigquery-dbt-project-500800
      dataset: dbt_project
      threads: 4
      keyfile: path\to\bq-key.json
      location: EU
```

```bash
cd sales_analytics
dbt run
dbt test
dbt docs generate && dbt docs serve
```

## Project Structure
data-modeling-dbt-bq/
├── .github/workflows/dbt_ci.yml
├── sales_analytics/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_sales.sql
│   │   │   ├── stg_customers.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── sources.yml
│   │   │   └── staging.yml
│   │   └── marts/
│   │       ├── fact_sales.sql
│   │       ├── dim_customer.sql
│   │       ├── dim_product.sql
│   │       ├── marts.yml
│   │       └── exposures.yml
│   └── dbt_project.yml
├── .gitignore
└── README.md

## Team
DEPI Data Engineering Program — Project 9: Data Modeling with dbt and BigQuery