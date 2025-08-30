import pandas as pd
from sqlalchemy import create_engine
from environment import *
import psycopg2

# CSV file path and table name
CSV_FILE_PATH = "ads_spend.csv"
TABLE_NAME = "tmp_ads_spend"

try:
    # Create a SQLAlchemy engine for connecting to PostgreSQL
    engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(host=HOST, database=DB_NAME, user=USER, password=PASSWORD, port=PORT)
    cur = conn.cursor()

    # Delete un processed data to make it atomic.
    cur.execute("delete from tmp_ads_spend where status = 'C';")
    conn.commit()

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(CSV_FILE_PATH)
    df['load_date'] = pd.Timestamp.now()
    df['source_file'] = CSV_FILE_PATH

    # Ingest data into PostgreSQL table
    df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

    # The MERGE statement
    merge_sql = """
        MERGE INTO ads_spend_data AS sd
        USING tmp_ads_spend AS ta
        ON sd.date = ta.date and sd.platform = ta.platform and sd.account = ta.account 
        and sd.campaign = ta.campaign and sd.country = ta.country and sd.device = ta.device 
        and ta.status = 'C'
        WHEN MATCHED THEN
            UPDATE SET
                spend = ta.spend, 
                clicks = ta.clicks, 
                impressions = ta.impressions,  
                conversions = ta.conversions,  
                load_date = ta.load_date,
                source_file = ta.source_file
        WHEN NOT MATCHED THEN
            INSERT (date, platform, account, campaign, country, device, spend, clicks, impressions, 
                    conversions, load_date, source_file)
            VALUES (ta.date, ta.platform, ta.account, ta.campaign, ta.country, ta.device, ta.spend, 
                    ta.clicks, ta.impressions, ta.conversions, ta.load_date, ta.source_file);
    """

    # Execute the MERGE statement
    cur.execute(merge_sql)

    # Delete un processed data to make it atomic.
    cur.execute("update tmp_ads_spend set status = 'P' where status = 'C';")

    conn.commit()

    print(f"Data from '{CSV_FILE_PATH}' successfully ingested into table '{TABLE_NAME}'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()