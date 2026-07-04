import os
import time
import duckdb
import pandas as pd
from sqlalchemy import create_engine

def migrate_oltp_to_parquet():
    print("🔌 Connecting to PostgreSQL OLTP layer to extract raw telemetry...")
    start_time = time.time()
    
    # 1. Establish connection to your Dockerized Postgres (port 5433)
    pg_engine = create_engine('postgresql://admin:telemetry_secret_pass@localhost:5433/raw_telemetry')
    
    # 2. Extract the data into memory using Pandas
    query = "SELECT * FROM raw_inference_logs;"
    df = pd.read_sql(query, pg_engine)
    print(f"📥 Extracted {len(df)} raw rows into local memory context.")
    
    # 3. Define target directories
    parquet_dir = "data"
    parquet_file_path = os.path.join(parquet_dir, "raw_inference_logs.parquet")
    
    # 4. Serialize to compressed Columnar Parquet format
    print("📦 Converting row-data and serializing to compressed columnar Parquet...")
    df.to_parquet(parquet_file_path, index=False, compression='snappy')
    print(f"💾 Parquet file successfully generated at: '{parquet_file_path}'")
    
    # 5. Initialize your analytical DuckDB layer and point it at the Parquet files
    print("🦆 Initializing local OLAP Warehouse layer (DuckDB)...")
    db_path = os.path.join(parquet_dir, "quackdb.db")
    con = duckdb.connect(db_path)
    
    # Create a native view inside DuckDB pointing directly to the Parquet file
    # used DuckDB to map a virtual view to your Parquet file
    con.execute(f"""
        CREATE OR REPLACE VIEW raw_logs AS 
        SELECT * FROM read_parquet('{parquet_file_path}');
    """)
    
    # Run a quick check aggregate query to verify it works
    # ran the very first DuckDB SQL query
    row_count = con.execute("SELECT COUNT(*) FROM raw_logs;").fetchone()[0]
    print(f"🎉 DuckDB OLAP layer initialized! View 'raw_logs' mapped to {row_count} records.")
    con.close()
    
    print(f"⏳ Migration completed successfully in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    migrate_oltp_to_parquet()