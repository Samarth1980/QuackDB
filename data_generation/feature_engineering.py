import os
import duckdb
import pandas as pd

def run_telemetry_feature_engineering():
    print("🔬 Initializing Hour 10: Telemetry Feature Engineering Pipeline...")
    
    # 1. Establish database connection
    db_path = os.path.join("data", "quackdb.db")
    con = duckdb.connect(db_path)
    
    # 2. Extract core fact records ordered chronologically
    print("📥 Fetching core fact metrics from main.fct_inference_requests...")
    query = """
    SELECT request_id, created_at, node_id, tokens_per_sec, ttft_ms, cost_usd
    FROM main.fct_inference_requests
    ORDER BY node_id, created_at;
    """
    df = con.execute(query).df()
    
    if df.empty:
        print("❌ Error: main.fct_inference_requests table is empty. Run dbt run first.")
        con.close()
        return

    print(f"✅ Successfully ingested {len(df):,} records into Pandas memory context.")
    
    # 3. Compute Window Functions Grouped by Node
    print("🧮 Calculating rolling 100-request statistics partitioned by node...")
    
    # Create our groupby object to isolate individual node time-series streams
    node_groups = df.groupby('node_id')
    
    # Compute 100-request rolling moving average for Throughput (TPS)
    df['rolling_avg_throughput_100'] = node_groups['tokens_per_sec'].transform(
        lambda x: x.rolling(window=100, min_periods=1).mean()
    )
    
    # Compute 100-request rolling P99 Quantile for Latency (TTFT)
    print("⚡ Mapping localized P99 tail anomalies...")
    df['rolling_p99_ttft_100'] = node_groups['ttft_ms'].transform(
        lambda x: x.rolling(window=100, min_periods=1).quantile(0.99)
    )
    
    # 4. Generate Anomaly Flags
    # Flag a request as a localized spike if its TTFT exceeds the recent 100-request P99 threshold
    df['is_p99_latency_spike'] = df['ttft_ms'] > df['rolling_p99_ttft_100']
    
    # 5. Write Features Back to the Analytical Warehouse
    print("📤 Materializing enriched feature matrix back to DuckDB...")
    
    # Register the dataframe as a virtual table within our active DuckDB context
    con.register('df_enriched_features', df)
    
    # Write the dataframe out into a permanent physical table
    con.execute("""
        CREATE OR REPLACE TABLE main.fct_enriched_telemetry AS 
        SELECT * FROM df_enriched_features;
    """)
    
    # Quick sanity check printout
    total_spikes = df['is_p99_latency_spike'].sum()
    print("📊 FEATURE ENGINEERING METRIC SUMMARY")
    print(f"Total Enriched Rows Processed   : {len(df):,}")
    print(f"Isolated Localized P99 Spikes   : {total_spikes:,} ({ (total_spikes/len(df))*100:.2f}% of traffic)")
    print("Target Schema Destination       : main.fct_enriched_telemetry")
    
    con.close()
    print("🎉 Feature engineering pipeline complete! Table successfully built.")

if __name__ == "__main__":
    run_telemetry_feature_engineering()
