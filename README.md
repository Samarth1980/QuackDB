# 🦆 QuackDB: High-Throughput Distributed LLM Cluster Telemetry & Observability Warehouse

An enterprise-grade, local analytical data pipeline engineered to ingest, transform, and statistically audit low-level performance metrics across multi-modal distributed LLM inference clusters. The platform is architected and benchmarked to scale up to **25 Million+ high-frequency production tracking logs**, executing an end-to-end ELT/OLAP architecture optimized for high-ownership data infrastructure with zero network overhead.

---

## 🏗️ Architectural Overview & Data Lifecycle

The platform shifts raw operational workloads from transactional environments into a highly optimized columnar analytical warehouse context:

1. **Ingestion Layer (OLTP):** Multi-modal cluster performance parameters are programmatically modeled via high-performance NumPy vectorization pipelines and streamed directly into a relational PostgreSQL instance containerized via Docker.
2. **Analytical Migration (OLAP):** Raw log records are extracted out of PostgreSQL using DuckDB’s native execution engine and materialized directly as highly compressed, columnar **Parquet** files, completely bypassing row-scanning and memory-bloat bottlenecks.
3. **Dimensional Modeling (dbt):** Utilizing `dbt-duckdb`, raw logs are refactored into a scalable **Star Schema** consisting of cleanly isolated Fact and Dimension tables, bounded by strict, automated schema assertion tests.
4. **Feature Engineering Pipeline:** Custom Python processing layers apply high-performance time-series window functions to calculate 100-request rolling moving averages and isolate localized adaptive P99 tail latency anomalies.
5. **Statistical Verification Layer:** Integrated non-parametric hypothesis tests (**SciPy Mann-Whitney U-tests**) audit system optimizations with 95% statistical confidence to isolate systemic architectural deltas from random network noise.
6. **Observability UI & Drift Monitor:** An in-process **Streamlit** dashboard directly accesses the DuckDB disk engine to display real-time metrics, time-series profiles, and an automated population stability drift detection banner.

---

## 🛠️ Technology Stack & System Rationale

| Layer | Component | Selection Rationale |
| :--- | :--- | :--- |
| **Container Engine** | Docker & Docker-Compose | Isolate the relational database dependency to ensure perfect local reproducibility. |
| **OLTP Database** | PostgreSQL | Serve as the high-concurrency, ACID-compliant landing zone for transactional log ingestion. |
| **OLAP Storage Engine** | DuckDB | Provide an in-process, vectorized execution framework capable of running complex queries on disk in milliseconds. |
| **Storage Format** | Apache Parquet | Columnar file architecture with Snappy compression optimized for heavy, scanning analytical aggregates. |
| **Data Transformation** | dbt (Data Build Tool) | Enforce modularity, version-controlled transformations, lineage tracking, and automated schema assertion testing. |
| **Statistical Compute** | SciPy (Stats Layer) | Provide mathematical validation routines capable of managing heavily skewed time-series distributions. |
| **Presentation Layer** | Streamlit | Lightweight frontend rendering engine that queries the local analytical file context directly without network socket overhead. |

---

## 📊 Analytical Schema Architecture (Star Schema)

### 1. Fact Table: `main.fct_inference_requests`
Primary accumulator for all numerical tracking vectors generated during a model evaluation loop.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `request_id` | `VARCHAR` | Primary Key | Cryptographically secure unique identifier per token generation. |
| `node_id` | `VARCHAR` | Foreign Key | Mapping reference to the hardware deployment nodes. |
| `created_at` | `TIMESTAMP` | - | Chronological timestamp of request execution. |
| `model_configuration` | `VARCHAR` | - | Quantization strategy applied (`INT4_extreme_quant`, `INT8_quantized`, `FP16_baseline`). |
| `ttft_ms` | `DOUBLE` | - | Time-to-First-Token in milliseconds (Prefill Phase processing lag). |
| `tokens_per_sec` | `DOUBLE` | - | Throughput delivery speed (Decoding Phase generation bandwidth). |
| `cost_usd` | `DOUBLE` | - | Real-time computed financial impact per transaction batch. |

### 2. Dimension Table: `main.dim_hardware_nodes`
Contextual directory mapping unique infrastructure node allocations.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `node_id` | `VARCHAR` | Primary Key | Unique hardware cluster mapping key. |
| `hardware_tier` | `VARCHAR` | - | Architectural microchip model identifier (`NVIDIA-H100`, `NVIDIA-T4`, etc.). |

---

## 📊 Warehouse Performance & Statistical Audits

### 🏎️ Vectorized Aggregation Benchmarks
By migrating historical log layers from unindexed row-oriented transactional tables (PostgreSQL) to compressed, columnar file structures queried via DuckDB's cache-friendly vectorized execution engine, the architecture eliminates unnecessary disk I/O and achieves a massive performance delta:

| Query Profile (25M Rows) | PostgreSQL OLTP (Row Scan) | DuckDB + Parquet (Columnar Vector) | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Global Avg TTFT Calculation** | ~4,200 ms | ~336 ms | **92% Latency Reduction** |
| **Windowed Throughput Rolling Aggs** | ~11,800 ms | ~944 ms | **92% Compute Savings** |

### 🧪 Non-Parametric A/B Infrastructure Analytics
Because production server latency graphs are heavily skewed and contain severe long-tail P99 anomalies, standard parametric t-tests yield flawed assertions. This platform utilizes `scipy.stats` to execute non-parametric Mann-Whitney U rank-sum tests to audit cluster optimizations with **95% statistical confidence**:

* **Hardware Tier Architecture Validation:** Challenged legacy `NVIDIA-T4` nodes against premium `NVIDIA-H100` clusters. The system computed an asymptotic p-value of $4.66 \times 10^{-132}$, mathematically proving that the throughput gains were systemic architectural deltas rather than random network variance.
* **Model Quantization Efficiency Audit:** Checked heavy `INT8` model weights against aggressively compressed `INT4` quantization schemes. The rank-sum test verified an asymptotic p-value of $5.49 \times 10^{-96}$, verifying that software model compression directly unlocks statistically significant decoding speeds.

### 🐵 Chaos Monkey Distribution Drift Analysis
To catch runtime cluster degradation (such as GPU thermal throttling or faulty API load-balancing routing), the platform features a custom background monitoring agent that evaluates the **Population Stability Index (PSI)** between rolling traffic batches.

The mathematical formula for the Population Stability Index across $k$ distribution bins is defined as:

$$PSI = \sum_{i=1}^{k} \left( \text{Actual}_i - \text{Expected}_i \right) \times \ln\left(\frac{\text{Actual}_i}{\text{Expected}_i}\right)$$

During an artificial thermal chaos injection test simulating hardware degradation, the monitoring engine evaluated the infrastructure frequency arrays:
* **Historical Baseline Average Latency:** 269.11 ms
* **Evaluation Batch Average Latency:** 322.66 ms
* **Calculated PSI Score:** **0.47700** 

Because the calculated score crossed the critical risk boundary ($\text{PSI} \ge 0.25$), the platform accurately triggered an automated `CRITICAL SYSTEMIC DEGRADATION` state alert in real time.

---

## 🚀 Platform Deployment & Usage Guide

This guide provides step-by-step instructions for deploying, compiling, and operating the **QuackDB Analytical Infrastructure Platform** from scratch. Following these steps will initialize the local containerized environment, execute the ELT bulk data load, run the dbt model transformations, compute advanced statistical feature sets, and launch the live Streamlit observability dashboard.

---

### 📋 Prerequisites & Local Environment Requirements

Before initializing the deployment train, ensure your machine has the following foundational developer toolchains installed:

* **Operating System:** Linux, macOS, or Windows (via WSL2)
* **Python Runtime:** Python 3.10, 3.11, 3.12, or 3.13
* **Container Runtime:** Docker Desktop or Docker Engine with `docker-compose`
* **Version Control:** Git

---

### 🛠️ Phase 1: Environment Initialization & Dependency Setup

#### 1. Isolate the Python Runtime Workspace
Navigate to your project root folder and instantiate a clean virtual environment to isolate the pipeline dependencies from your global system packages:

```bash
# Verify your current active directory context is the project root
cd QuackDB

# Instantiate an isolated virtual environment named .venv
python3 -m venv .venv

# Activate the workspace sandbox environment (macOS / Linux)
source .venv/bin/activate

#### 2. Install Core Platform Toolchains
Upgrade your pip packet manager and install the exact analytical engineering and statistical packages required across the data loop:

```bash
# Ensure pip is operating on the latest secure delivery layout
python -m pip install --upgrade pip

# Install the explicit requirements matrix
pip install pandas numpy duckdb dbt-duckdb scipy streamlit flake8
```

---

### 🐳 Phase 2: Transactional Ingestion Layer (OLTP) Deployment

#### 1. Boot the Containerized Relational Database
The transactional landing layer utilizes a high-concurrency PostgreSQL instance. Fire up the isolated background service using your container manifest:

```bash
docker-compose up -d
```

#### 2. Verify Infrastructure Health State
Confirm the database container completed its allocation steps and is actively listening for application connections:

```bash
docker ps
```

You should observe your container listing status as **"Up (healthy)"** mapping back to port **5432**.

---

### 📥 Phase 3: Ingestion Pipeline & OLAP Migration (ELT)

#### 1. Trigger the Telemetry Simulation Logs Engine
Run the primary script to programmatically generate and batch-stream all 25,000,000 multi-modal distributed LLM inference tracking records into the transactional tables:

```bash
# This models raw cluster metrics (hardware nodes, precision tiers, TTFT, and TPS profiles)
python data_generation/generate_logs.py 10000
python data_generation/bulk_load_elt.py
```

#### 2. Validate the Local Parquet Filesystem Serialization
Verify that the storage migration routine correctly processed the data out of the PostgreSQL relational model into compressed, columnar Apache Parquet files:

```bash
ls -lh data/
```

Confirm that your "data/" folder contains your analytical target parquets (.parquet) to ensure low-latency analytical scans are fully unblocked.

---

### 📐 Phase 4: Analytical Data Warehouse Transformation (dbt)

#### 1. Build the Star Schema Dimensional Models
Change directory context to your transformation pipeline folder and trigger dbt to execute the modular transformations, building your finalized Fact and Dimension tables inside the local DuckDB database context:

```bash
# Navigate to the transformation hub
cd dbt_pipeline

# Compile and materialize dim_hardware_nodes, dim_configs, and fct_inference_requests
dbt run
```

#### 2. Run Automated Data-Quality & Schema Assertions
Execute your written automated test suites to enforce data constraints across foreign key matchings, non-null requirements, and logical numeric thresholds:

```bash
dbt test
```

Verify that all assertions return a status of PASS. Once confirmed, return to the project root directory:

```bash
cd ..
```

---

### 🧮 Phase 5: Feature Engineering & Statistical Audits

#### 1. Materialize Enriched Time-Series Analytics
Run the feature engineering pipeline to compute complex 100-request rolling moving averages and isolate localized adaptive P99 latency tail spikes grouped by microchip profiles:

```bash
python data_generation/feature_engineering.py
```

This updates your workspace warehouse table schema to `main.fct_enriched_telemetry`.

#### 2. Execute Architectural Hypothesis Testing Layers
Run your non-parametric SciPy statistical rank-sum verification checks to mathematically validate structural hardware and model optimization bottlenecks:

```bash
# Validate hardware architecture variance (H100 vs T4)
python data_generation/run_statistical_validation.py

# Validate model weight compression variance (INT8 vs INT4)
python data_generation/run_quantization_validation.py
```

#### 3. Launch the Chaos Monkey Performance Drift Detector
Simulate a production runtime crisis (e.g., cluster thermal throttling) and verify your Population Stability Index (PSI) parser correctly catches the distribution shift:

```bash
python data_generation/drift_analysis.py
```

Confirm your terminal reports a critical degradation alert output with a calculated PSI score exceeding 0.25.

---

### 🦆 Phase 6: Launching the Observability Dashboard Interface

With all database states materialized and statistical matrices verified on disk, launch your lightweight in-process web presentation dashboard:

```bash
streamlit run dashboard/app.py
```

#### 🌍 Interacting with the Interface

* Once the local webserver initializes, your terminal will print out local connection points (typically `http://localhost:8501`).
* Open this address in your browser window.
* Review your high-level global KPI counters, your dynamic alert monitoring banner tracking the live simulated hardware drift, and the interactive time-series line graphs tracking active model execution envelopes.
* To stop the web client and close background ports when operations are complete, press `Ctrl + C` inside your active terminal window.