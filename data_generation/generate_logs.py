import os
import time
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def generate_telemetry_dataset(num_records=25000000):
    print(f"⚡ Vectorizing {num_records:,} raw LLM inference telemetry logs...")
    start_time = time.time()
    
    # 1. Define hardware clusters and configuration states
    nodes = ['node_us_east_01', 'node_eu_west_02', 'node_asia_pacific_03', 'node_local_edge_04']
    gpu_types = ['NVIDIA-H100', 'AMD-MI300X', 'NVIDIA-T4', 'Apple-M2-Max']
    
    configs = ['FP16_baseline', 'INT8_quantized', 'INT4_extreme_quant']
    algorithms = ['Round-Robin', 'Inverse-Weight-Custom']
    
    # 2. Vectorized generation using NumPy indices for safety and speed
    np.random.seed(42)
    
    # Generate random positional indices instead of strings directly
    node_indices = np.random.choice(len(nodes), size=num_records, p=[0.4, 0.3, 0.2, 0.1])
    generated_nodes = np.array(nodes)[node_indices]
    generated_gpus = np.array(gpu_types)[node_indices]
    
    generated_configs = np.random.choice(configs, size=num_records, p=[0.3, 0.5, 0.2])
    generated_algos = np.random.choice(algorithms, size=num_records, p=[0.5, 0.5])
    
    # Generate timestamp arrays spanning the past 48 hours
    end_ts = time.time()
    start_ts = end_ts - (48 * 3600)
    timestamps = pd.to_datetime(np.random.uniform(start_ts, end_ts, size=num_records), unit='s')
    
    # 3. Model complex math distributions for metrics (Fully Vectorized)
    base_latency = np.random.exponential(scale=150, size=num_records) + 50 
    
    # Replaced the loop with vectorized mask applications
    base_latency = np.where(generated_configs == 'INT4_extreme_quant', base_latency * 0.45, base_latency)
    base_latency = np.where(generated_gpus == 'NVIDIA-T4', base_latency * 1.8, base_latency)
            
    # Add network overhead variance
    network_hop_delay = np.clip(np.random.normal(loc=45, scale=15, size=num_records), 5, None)
    serialization_overhead = np.random.gamma(shape=2, scale=10, size=num_records)
    
    # Calculate operational KPIs
    ttft_ms = base_latency + network_hop_delay + serialization_overhead
    tokens_count = np.random.randint(32, 1024, size=num_records)
    tokens_per_sec = tokens_count / (ttft_ms / 1000.0)
    
    # Vectorized Cost Calculation
    cost_mapping = {'NVIDIA-H100': 0.002, 'AMD-MI300X': 0.0012, 'NVIDIA-T4': 0.0004, 'Apple-M2-Max': 0.0001}
    cost_per_token = np.vectorize(cost_mapping.get)(generated_gpus)
    cost_per_token = np.where(generated_configs == 'INT4_extreme_quant', cost_per_token * 0.7, cost_per_token)
    total_cost = tokens_count * cost_per_token
    
    # 4. Inject simulated error anomalies
    status_codes = np.ones(num_records, dtype=int) * 200
    error_indices = np.random.choice(num_records, size=int(num_records * 0.008), replace=False)
    status_codes[error_indices] = 500
    
    # Build the final comprehensive DataFrame (Cleaned up modern NumPy namespace)
    df = pd.DataFrame({
        'request_id': np.char.add("req_", np.char.zfill(np.arange(num_records).astype(str), 7)),
        'timestamp': timestamps,
        'node_id': generated_nodes,
        'hardware_tier': generated_gpus,
        'model_configuration': generated_configs,
        'load_balancer_algo': generated_algos,
        'tokens_processed': tokens_count,
        'time_to_first_token_ms': ttft_ms,
        'tokens_per_second': tokens_per_sec,
        'network_delay_ms': network_hop_delay,
        'serialization_overhead_ms': serialization_overhead,
        'estimated_cost_usd': total_cost,
        'http_status_code': status_codes
    })
    
    print(f"✅ Data vectorized completely in {time.time() - start_time:.2f} seconds.")
    return df

def stream_to_postgres(df):
    print("🚀 Initiating Bulk Connection to PostgreSQL OLTP Layer...")
    engine = create_engine('postgresql://admin:telemetry_secret_pass@localhost:5433/raw_telemetry')
    
    start_time = time.time()
    df.to_sql('raw_inference_logs', engine, if_exists='replace', index=False, chunksize=100000)
    print(f"💾 Successfully loaded {len(df):,} rows into 'raw_inference_logs' in {time.time() - start_time:.2f} seconds!")

if __name__ == "__main__":
    import sys
    rows = int(sys.argv[1]) if len(sys.argv) > 1 else 25000000
    telemetry_df = generate_telemetry_dataset(rows)
    stream_to_postgres(telemetry_df)