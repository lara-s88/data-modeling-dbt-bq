from google.cloud import bigquery
from google.oauth2 import service_account
import os

PROJECT_ID   = "bigquery-dbt-project-500800"
DATASET_ID   = "dbt_project"
KEYFILE_PATH = os.path.join(os.path.dirname(__file__), "bq-key.json")

credentials = service_account.Credentials.from_service_account_file(
    KEYFILE_PATH,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
client = bigquery.Client(project=PROJECT_ID, credentials=credentials)

print("Connected to BigQuery successfully")

RAW_SALES_SQL = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.raw_sales` AS
SELECT
  (a * 1500 + b) AS order_id,
  CAST(FLOOR(RAND() * 1000) AS INT64) AS customer_id,
  CAST(FLOOR(RAND() * 50) AS INT64) AS product_id,
  ROUND(RAND() * 500, 2) AS amount,
  CAST(FLOOR(RAND() * 5) + 1 AS INT64) AS quantity,
  DATE_SUB(CURRENT_DATE(), INTERVAL CAST(FLOOR(RAND() * 730) AS INT64) DAY) AS order_date,
  ['credit_card','paypal','debit_card','bank_transfer'][OFFSET(CAST(FLOOR(RAND()*4) AS INT64))] AS payment_method
FROM
  UNNEST(GENERATE_ARRAY(0, 999)) AS a,
  UNNEST(GENERATE_ARRAY(0, 1499)) AS b;
"""

RAW_CUSTOMERS_SQL = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.raw_customers` AS
SELECT
  customer_id,
  CONCAT('Customer_', CAST(customer_id AS STRING)) AS customer_name,
  CONCAT('customer', CAST(customer_id AS STRING), '@email.com') AS email,
  ['North','South','East','West'][OFFSET(MOD(customer_id, 4))] AS region,
  DATE_SUB(CURRENT_DATE(), INTERVAL MOD(customer_id, 1000) DAY) AS signup_date
FROM UNNEST(GENERATE_ARRAY(0, 999)) AS customer_id;
"""

RAW_PRODUCTS_SQL = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.raw_products` AS
SELECT
  product_id,
  CONCAT('Product_', CAST(product_id AS STRING)) AS product_name,
  ['Electronics','Clothing','Food','Sports','Books'][OFFSET(MOD(product_id, 5))] AS category,
  ROUND(10 + (RAND() * 490), 2) AS cost_price
FROM UNNEST(GENERATE_ARRAY(0, 49)) AS product_id;
"""

tables = [
    ("raw_sales", RAW_SALES_SQL, "1,500,000 rows"),
    ("raw_customers", RAW_CUSTOMERS_SQL, "1,000 rows"),
    ("raw_products", RAW_PRODUCTS_SQL, "50 rows"),
]

for table_name, sql, expected_rows in tables:
    print(f"Creating {table_name} ({expected_rows})...")
    query_job = client.query(sql)
    query_job.result()
    print(f"{table_name} created successfully")

print("All raw tables created successfully!")