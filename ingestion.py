import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# These would be environment variables, but will be changed after challenge is finished
DB_NAME = "postgres"
USER = "postgres"
PASSWORD = "#Test2025"
HOST = "db.bkzdsijontjmmccnfqfi.supabase.co"
PORT = "5432"

# CSV file path and table name
CSV_FILE_PATH = "ads_spend.csv"
TABLE_NAME = "tmp_ads_spend"

try:
    # Create a SQLAlchemy engine for connecting to PostgreSQL
    engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(CSV_FILE_PATH)
    df['load_date'] = pd.Timestamp.now()
    df['source_file'] = CSV_FILE_PATH

    # Ingest data into PostgreSQL table
    df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

    print(f"Data from '{CSV_FILE_PATH}' successfully ingested into table '{TABLE_NAME}'.")

except Exception as e:
    print(f"An error occurred: {e}")