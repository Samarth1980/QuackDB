import os
import duckdb
import pandas as pd
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="QuackDB | LLM Cluster Telemetry",
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

# 3. Main Dashboard Header
st.title("🦆 QuackDB Infrastructure Analytics Platform")
st.markdown("### Real-Time LLM Production Cluster Performance & Telemetry Warehouse")
st.write("---")

# 4. Fetch Global Metrics for Top KPI Cards
kpi_query = """
SELECT 
    COUNT(*) as total_reqs,
    ROUND(AVG(ttft_ms), 1) as avg_ttft,
    ROUND(AVG(tokens_per_sec), 1) as avg_throughput,
    ROUND(SUM(cost_usd), 2) as total_cost
FROM main.fct_inference_requests;
"""

try:
    kpi_df = get_warehouse_data(kpi_query)
    
    # Display KPIs in 4 parallel columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Logged Requests", f"{kpi_df['total_reqs'][0]:,}")
    col2.metric("Global Avg TTFT", f"{kpi_df['avg_ttft'][0]} ms")
    col3.metric("Global Avg Throughput", f"{kpi_df['avg_throughput'][0]} tok/s")
    col4.metric("Total Financial Bill", f"${kpi_df['total_cost'][0]:,}")
    
    st.write("---")
    
    # 5. Visualizations Section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### 💻 Throughput Speed by Hardware Chip Tier")
        hardware_query = """
        SELECT 
            d.hardware_tier,
            ROUND(AVG(f.tokens_per_sec), 1) as avg_throughput_tok_sec
        FROM main.fct_inference_requests f
        JOIN main.dim_hardware_nodes d ON f.node_id = d.node_id
        GROUP BY d.hardware_tier
        ORDER BY avg_throughput_tok_sec DESC;
        """
        hw_df = get_warehouse_data(hardware_query)
        # Render clean bar chart using native streamlit components
        st.bar_chart(data=hw_df, x="hardware_tier", y="avg_throughput_tok_sec", color="#4682B4")
        
    with chart_col2:
        st.markdown("#### ⚡ Latency vs Cost by Quantization Model Config")
        quant_query = """
        SELECT 
            model_configuration,
            ROUND(AVG(ttft_ms), 1) as avg_latency_ms,
            ROUND(AVG(cost_usd), 4) as avg_cost_per_request_usd
        FROM main.fct_inference_requests
        GROUP BY model_configuration;
        """
        quant_df = get_warehouse_data(quant_query)
        # Render an analytical table profile for direct cross-comparison
        st.dataframe(quant_df, use_container_width=True, hide_index=True)
    
except Exception as e:
    st.error(f"❌ Failed to connect to analytical warehouse: {e}")
    st.info("Ensure your dbt models have been successfully run and materialized into the 'main' schema.")