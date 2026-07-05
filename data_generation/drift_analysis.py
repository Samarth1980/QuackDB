import os
import duckdb
import numpy as np
import pandas as pd

def calculate_psi(baseline, target, num_bins=10):
    """Calculates the Population Stability Index (PSI) between two distributions."""
    # 1. Establish quantile-based boundaries using the baseline dataset
    try:
        # Use qcut to create equal-sized frequency bins from baseline
        _, bins = pd.qcut(baseline, q=num_bins, retbins=True, labels=False, duplicates='drop')
    except ValueError:
        # Fallback to linear spacing if distribution has zero variance
        bins = np.linspace(baseline.min(), baseline.max(), num_bins + 1)
        
    # Adjust outer boundaries to encapsulate potential target outliers
    bins[0] = -np.inf
    bins[-1] = np.inf
    
    # 2. Bucket both populations into the identical bin infrastructure
    baseline_counts = pd.cut(baseline, bins=bins).value_counts().sort_index()
    target_counts = pd.cut(target, bins=bins).value_counts().sort_index()
    
    # 3. Convert absolute counts to relative percentages
    expected_pct = baseline_counts / len(baseline)
    actual_pct = target_counts / len(target)
    
    # 4. Inject a tiny epsilon boundary adjustment to completely avoid division by zero or log(0)
    expected_pct = expected_pct.replace(0, 1e-4)
    actual_pct = actual_pct.replace(0, 1e-4)
    
    # 5. Compute the formal mathematical PSI summation
    psi_value = np.sum((actual_pct - expected_pct) * np.log(actual_pct / expected_pct))
    return psi_value

def execute_drift_simulation_engine():
    print("🐵 Initializing Hour 12: Chaos Monkey Drift Simulation Engine...")
    
    # Connect to database warehouse
    db_path = os.path.join("data", "quackdb.db")
    con = duckdb.connect(db_path)
    
    print("📥 Ingesting baseline population metrics from main warehouse...")
    baseline_df = con.execute("SELECT tokens_per_sec, ttft_ms FROM main.fct_inference_requests;").df()
    con.close()
    
    if baseline_df.empty:
        print("❌ Error: Analytical warehouse baseline is empty.")
        return
        
    # Isolate our historical baseline distribution
    baseline_ttft = baseline_df['ttft_ms']
    
    print(f"📊 Baseline established with {len(baseline_ttft):,} operational logs.")
    print(f"   • Historical Avg Latency: {baseline_ttft.mean():.2f} ms")
    
    # -------------------------------------------------------------------------
    # CHAOS MONKEY SIMULATION: Generate recent degraded production traffic
    # -------------------------------------------------------------------------
    print("\n⚡ Simulating recent production batch with artificial thermal degradation...")
    np.random.seed(42)
    sample_size = 50000
    
    # Copy the core shape of baseline but artificially shift the median and spread out variance
    # This simulates nodes experiencing severe thermal throttling or packet routing degradation
    simulated_healthy = np.random.normal(loc=baseline_ttft.mean(), scale=baseline_ttft.std(), size=int(sample_size * 0.65))
    simulated_drifted = np.random.normal(loc=baseline_ttft.mean() * 1.45, scale=baseline_ttft.std() * 1.8, size=int(sample_size * 0.35))
    
    target_ttft = pd.Series(np.concatenate([simulated_healthy, simulated_drifted]))
    # Enforce realistic boundaries (latency cannot be negative)
    target_ttft = target_ttft.clip(lower=10)
    
    print(f"📥 Target test population generated with {len(target_ttft):,} recent evaluation rows.")
    print(f"   • Current Evaluation Traffic Avg Latency: {target_ttft.mean():.2f} ms")
    
    # -------------------------------------------------------------------------
    # PSI CALCULATOR EVALUATION LAYER
    # -------------------------------------------------------------------------
    print("\n🧮 Compiling Population Stability Index (PSI) matrix across bins...")
    psi_score = calculate_psi(baseline_ttft, target_ttft, num_bins=10)
    
    print("\n=======================================================")
    print("🚨 PRODUCTION INFRASTRUCTURE DRIFT METRIC REPORT")
    print("=======================================================")
    print(f"Calculated Population Stability Index: {psi_score:.5f}")
    
    print("-------------------------------------------------------")
    if psi_score < 0.1:
        print("✅ SYSTEM STATUS: STABLE")
        print("   The recent production traffic matches historical distributions baseline.")
    elif 0.1 <= psi_score < 0.25:
        print("⚠️ SYSTEM STATUS: MODERATE DRIFT DETECTED")
        print("   Minor structural changes observed. Schedule infrastructure investigation.")
    else:
        print("🚨 SYSTEM STATUS: CRITICAL SYSTEMIC DEGRADATION")
        print("   Significant distribution shift caught (PSI >= 0.25).")
        print("   Action required: Check cluster telemetry, node thermals, and API routing health.")
    print("=======================================================\n")

if __name__ == "__main__":
    execute_drift_simulation_engine()