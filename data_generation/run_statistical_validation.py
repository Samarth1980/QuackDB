import os
import duckdb
import pandas as pd
from scipy import stats

def execute_hardware_hypothesis_test():
    print("🧪 Initializing Advanced Statistical Validation Layer (SciPy)...")
    
    # 1. Mount the local DuckDB warehouse file
    db_path = os.path.join("data", "quackdb.db")
    con = duckdb.connect(db_path)
    
    # 2. Extract performance records directly from our dbt structured marts
    query = """
    SELECT f.ttft_ms, d.hardware_tier 
    FROM main.fct_inference_requests f
    JOIN main.dim_hardware_nodes d ON f.node_id = d.node_id
    WHERE d.hardware_tier IN ('NVIDIA-H100', 'NVIDIA-T4');
    """
    df = con.execute(query).df()
    con.close()
    
    # Isolate sample arrays
    h100_latencies = df[df['hardware_tier'] == 'NVIDIA-H100']['ttft_ms']
    t4_latencies = df[df['hardware_tier'] == 'NVIDIA-T4']['ttft_ms']
    
    print(f"\n📊 Extracted sample distributions from database context:")
    print(f"   • NVIDIA-H100 Population Size: {len(h100_latencies):,}")
    print(f"   • NVIDIA-T4   Population Size: {len(t4_latencies):,}")
    
    # 3. Compute non-parametric Mann-Whitney U test (two-sided)
    print("\n🧮 Computing Mann-Whitney U Test ranks across populations...")
    u_statistic, p_value = stats.mannwhitneyu(h100_latencies, t4_latencies, alternative='two-sided')
    
    print("🔬 INDUSTRIAL STATISTICAL HYPOTHESIS TEST REPORT")
    print(f"Computed U-Statistic : {u_statistic:,.2f}")
    print(f"Asymptotic P-Value   : {p_value}")
    
    alpha = 0.05
    if p_value < alpha:
        print("🚨 CRITICAL CONCLUSION: REJECT THE NULL HYPOTHESIS (H₀)")
        print(f"   The latency difference between the tiers is statistically significant (p < {alpha}).")
        print("   The variance is due to systemic architectural delta, NOT random network noise.")
    else:
        print("✅ CONCLUSION: FAIL TO REJECT THE NULL HYPOTHESIS (H₀)")
        print("   No statistically significant variance detected between performance populations.")

if __name__ == "__main__":
    execute_hardware_hypothesis_test()
