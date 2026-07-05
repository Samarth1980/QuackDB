import os
import duckdb
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="QuackDB | Cluster Observability",
    page_icon="🦆",
    layout="wide"
)

# 2. Database Connection Helper
def get_warehouse_data(query):
    db_path = os.path.join("data", "quackdb.db")
    con = duckdb.connect(db_path, read_only=True)
    df = con.execute(query).df()
    con.close()
    return df

# 3. Header Infrastructure
st.title("🦆 QuackDB Enterprise Observability Engine")
st.markdown("### Real-Time Core Telemetry Warehouse & Advanced Production Drift Monitor")

# -------------------------------------------------------------------------
# LIVE ALERTS LAYER: Population Stability Index Banner
# -------------------------------------------------------------------------
# Hardcoded from your Hour 12 analysis to simulate a production monitoring loop
psi_score = 0.47723 
st.write("---")
st.error(
    f"🚨 **CRITICAL INFRASTRUCTURE ALERT:** Systemic distribution drift caught! "
    f"Calculated Population Stability Index (PSI): **{psi_score:.5f}** (Threshold >= 0.25). "
    f"Potential thermal throttling or packet routing anomalies detected across active clusters."
)

# 4. Fetch Global Metrics for Top KPI Cards (Using the new enriched table)
kpi_query = """
SELECT 
    COUNT(*) as total_reqs,
    ROUND(AVG(ttft_ms), 1) as avg_ttft,
    SUM(CASE WHEN is_p99_latency_spike = TRUE THEN 1 ELSE 0 END) as total_spikes,
    ROUND(SUM(cost_usd), 2) as total_cost
FROM main.fct_enriched_telemetry;
"""

try:
    kpi_df = get_warehouse_data(kpi_query)
    
    # Display KPIs in 4 parallel columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Logged Requests", f"{kpi_df['total_reqs'][0]:,}")
    col2.metric("Global Avg TTFT", f"{kpi_df['avg_ttft'][0]} ms")
    col3.metric("Anomalous P99 Spikes Caught", f"{kpi_df['total_spikes'][0]:,}", delta="- Localized Adaptive Threshold", delta_color="inverse")
    col4.metric("Total Infrastructure Cost", f"${kpi_df['total_cost'][0]:,}")
    
    st.write("---")
    
    # 5. Interactive Visualizations Sidebar/Filters
    st.markdown("#### 🛠️ Localized Time-Series Telemetry (Last 500 Requests)")
    
    # Query to pull a slice of the rolling features for data visualization
    time_series_query = """
    SELECT 
        created_at,
        ttft_ms,
        rolling_p99_ttft_100,
        rolling_avg_throughput_100
    FROM main.fct_enriched_telemetry
    ORDER BY created_at DESC
    LIMIT 500;
    """
    ts_df = get_warehouse_data(time_series_query)
    
    # Split charts into two columns
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Adaptive P99 Latency Boundary vs Raw TTFT**")
        # Line chart showing raw latency vs the rolling 100-request safety envelope
        st.line_chart(data=ts_df, x="created_at", y=["ttft_ms", "rolling_p99_ttft_100"], color=["#1f77b4", "#ff7f0e"])
        
    with chart_col2:
        st.markdown("**100-Request Rolling Throughput Moving Average (TPS)**")
        # Line chart tracing the rolling moving average profile
        st.line_chart(data=ts_df, x="created_at", y="rolling_avg_throughput_100", color="#2ca02c")

except Exception as e:
    st.error(f"❌ Failed to render telemetry dashboard: {e}")