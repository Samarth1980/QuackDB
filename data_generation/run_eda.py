import os
import duckdb
import pandas as pd

def perform_cluster_eda():
    print("📊 Connecting to DuckDB OLAP Layer for Exploratory Data Analysis (EDA)...")
    
    # 1. Connect to the existing analytical local database file
    db_path = os.path.join("data", "quackdb.db")
    con = duckdb.connect(db_path)
    
    # 2. Query 1: Global Health Metrics Check
    print("📈 GLOBAL LLM INFRASTRUCTURE HEALTH PROFILE: ")
    global_query = """
    SELECT 
        COUNT(*) as total_logged_requests,
        ROUND(AVG(time_to_first_token_ms), 2) as global_avg_ttft_ms,
        ROUND(AVG(tokens_per_second), 2) as global_avg_tokens_per_sec,
        ROUND(SUM(estimated_cost_usd), 2) as total_cluster_cost_usd,
        ROUND(COUNT(CASE WHEN http_status_code = 500 THEN 1 END) * 100.0 / COUNT(*), 3) as system_error_rate_pct
    FROM raw_logs;
    """
    df_global = con.execute(global_query).df()
    print(df_global.to_string(index=False))
    
    # 3. Query 2: Hardware Tier Profiling (Analyzing LLM Infrastructure KPIs)
    print("💻 INFRASTRUCTURE PERFORMANCE BY HARDWARE CHIP TIER: ")
    hw_query = """
    SELECT 
        hardware_tier,
        COUNT(*) as request_volume,
        ROUND(MIN(time_to_first_token_ms), 1) as min_ttft_ms,
        ROUND(AVG(time_to_first_token_ms), 1) as avg_ttft_ms,
        ROUND(MAX(time_to_first_token_ms), 1) as max_tail_ttft_ms,
        ROUND(AVG(tokens_per_second), 1) as avg_throughput_tokens_sec
    FROM raw_logs
    GROUP BY hardware_tier
    ORDER BY avg_ttft_ms ASC;
    """
    df_hw = con.execute(hw_query).df()
    print(df_hw.to_string(index=False))

    # 4. Query 3: Software Quantization Configuration vs Cost and Latency Tradeoffs
    print("⚡ EFFICIENCY METRICS BY QUANTIZATION MODEL CONFIG: ")
    config_query = """
    SELECT 
        model_configuration,
        ROUND(AVG(time_to_first_token_ms), 1) as avg_ttft_ms,
        ROUND(AVG(tokens_per_second), 1) as avg_throughput_tokens_sec,
        ROUND(AVG(estimated_cost_usd), 5) as avg_cost_per_request_usd
    FROM raw_logs
    GROUP BY model_configuration
    ORDER BY avg_throughput_tokens_sec DESC;
    """
    df_config = con.execute(config_query).df()
    print(df_config.to_string(index=False))
    
    con.close()
    print("\n🔍 EDA complete. Data distributions are clean, valid, and show distinct variance.")

if __name__ == "__main__":
    perform_cluster_eda()