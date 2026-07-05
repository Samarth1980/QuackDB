import os
import duckdb
import pandas as pd
from scipy import stats

def execute_quantization_hypothesis_test():
    print("🧪 Initializing Hour 11: Quantization Performance Verification Layer...")
    
    # 1. Connect to local DuckDB warehouse
    db_path = os.path.join("data", "quackdb.db")
    con = duckdb.connect(db_path)
    
    # 2. Extract throughput metrics from our dbt structured fact table
    query = """
    SELECT tokens_per_sec, model_configuration 
    FROM main.fct_inference_requests
    WHERE model_configuration IN ('INT8', 'INT4');
    """
    df = con.execute(query).df()
    con.close()
    
    # Isolate populations
    int8_throughput = df[df['model_configuration'] == 'INT8']['tokens_per_sec']
    int4_throughput = df[df['model_configuration'] == 'INT4']['tokens_per_sec']
    
    print(f"\n📊 Extracted sample populations from main warehouse:")
    print(f"   • INT8 Config Sample Size: {len(int8_throughput):,}")
    print(f"   • INT4 Config Sample Size: {len(int4_throughput):,}")
    
    # 3. Compute Non-Parametric Mann-Whitney U Test
    print("\n🧮 Computing rank-sum statistics across optimization tiers...")
    u_statistic, p_value = stats.mannwhitneyu(int8_throughput, int4_throughput, alternative='two-sided')
    
    print("\n=======================================================")
    print("🔬 QUANTIZATION EFFICIENCY HYPOTHESIS REPORT")
    print("=======================================================")
    print(f"Computed U-Statistic : {u_statistic:,.2f}")
    print(f"Asymptotic P-Value   : {p_value}")
    
    alpha = 0.05  # 95% Confidence Interval Boundary
    print("-------------------------------------------------------")
    if p_value < alpha:
        print("🚨 CRITICAL CONCLUSION: REJECT THE NULL HYPOTHESIS (H₀)")
        print(f"   The throughput delta between INT8 and INT4 is mathematically significant (p < {alpha}).")
        print("   Quantization compression directly impacts inference speeds.")
    else:
        print("✅ CONCLUSION: FAIL TO REJECT THE NULL HYPOTHESIS (H₀)")
        print("   No statistically significant difference in speed distributions detected.")
    print("=======================================================\n")

if __name__ == "__main__":
    execute_quantization_hypothesis_test()