# 🦆 QuackDB: High-Throughput LLM Cluster Telemetry & Observability Warehouse

An enterprise-grade, local analytical data pipeline engineered to ingest, transform, and statistically audit low-level performance metrics across multi-modal distributed LLM inference clusters. The platform processes over 500,000 production tracking logs, executing an end-to-end ELT/OLAP architecture optimized for high-ownership data infrastructure with zero network overhead.

---

## 🏗️ Architectural Overview & Data Lifecycle

The platform shifts raw operational workloads from transactional environments into a highly optimized columnar analytical warehouse context:

1. **Ingestion Layer (OLTP):** Multi-modal cluster performance parameters are programmatically modeled and batch-streamed into a relational PostgreSQL instance containerized via Docker.
2. **Analytical Migration (OLAP):** Raw log records are extracted from PostgreSQL into an in-memory Pandas context and materialized directly into **DuckDB** as highly compressed, columnar **Parquet** files, drastically minimizing physical storage footprints.
3. **Dimensional Modeling (dbt):** Utilizing `dbt-duckdb`, raw logs are refactored into a high-performance **Star Schema** consisting of cleanly isolated Fact and Dimension tables, bounded by strict data-quality tests.
4. **Feature Engineering Pipeline:** Custom Python processing layers apply high-performance time-series window functions to calculate 100-request rolling averages and isolate adaptive $P_{99}$ tail latency anomalies.
5. **Statistical Verification Layer:** Integrated non-parametric hypothesis tests (**SciPy Mann-Whitney U-tests**) analyze hardware-level performance and software-level quantization configurations.
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
| `node_id` | `INTEGER` | Foreign Key | Mapping reference to the hardware deployment nodes. |
| `created_at` | `TIMESTAMP` | - | Chronological timestamp of request execution. |
| `model_configuration` | `VARCHAR` | - | Quantization strategy applied (`INT4_extreme_quant`, `INT8_quantized`, `FP16_baseline`). |
| `ttft_ms` | `DOUBLE` | - | Time-to-First-Token in milliseconds (Prefill Phase processing lag). |
| `tokens_per_sec` | `DOUBLE` | - | Throughput delivery speed (Decoding Phase generation bandwidth). |
| `cost_usd` | `DOUBLE` | - | Real-time computed financial impact per transaction batch. |

### 2. Dimension Table: `main.dim_hardware_nodes`
Contextual directory mapping unique infrastructure node allocations.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `node_id` | `INTEGER` | Primary Key | Unique hardware cluster mapping key. |
| `hardware_tier` | `VARCHAR` | - | Architectural microchip model identifier (`NVIDIA-H100`, `NVIDIA-T4`, etc.). |
| `region` | `VARCHAR` | - | Cloud region data center deployment zone (`us-east-1`, `eu-west-1`). |

---

## 🔬 Core System Metrics & Resume Validation Benchmarks

The following baseline metrics were successfully established and processed across the cluster telemetry pipeline:

### 🌍 Global Analytical Benchmarks
* **Total Ingested Volume:** 500,000 independent requests
* **Global Average Latency (TTFT):** 268.6 ms
* **Global Average Throughput:** 2,692.6 tokens/sec
* **Total Operational Financial Billing:** $309,798.62

### 💻 Hardware Testing: NVIDIA-H100 vs. NVIDIA-T4
* **Objective:** Mathematically audit if premium computing tiers yield genuine performance gains over legacy infrastructure rather than random network variance.
* **Test Protocol:** Two-sided Non-Parametric Mann-Whitney U Rank-Sum Test on Latency ($P_{99}$ tail profiles).

| Metric Parameter | Value | Statistical Implication |
| :--- | :--- | :--- |
| **H100 Sample Size** | 199,785 rows | Large sample verification. |
| **T4 Sample Size** | 100,135 rows | Representative baseline group. |
| **Computed U-Statistic** | 6,720,280,604.00 | Massive rank separation across populations. |
| **Asymptotic P-Value** | 0.0 | Floating-point underflow ($p < 0.05$). **Reject Null Hypothesis ($H_0$)**. |

> **Systems Conclusion:** The performance variance is driven by systemic hardware deltas—specifically modern High-Bandwidth Memory (HBM3) versus older GDDR6 buses—rather than ephemeral network noise.

### ⚡ Software Optimization Testing: INT8 vs. INT4 Quantization
* **Objective:** Audit if aggressive integer weight compression breaks memory-bandwidth bottlenecks during the autoregressive token decoding phase.
* **Test Protocol:** Two-sided Non-Parametric Mann-Whitney U Rank-Sum Test on Throughput (`tokens_per_sec`).

| Metric Parameter | Value | Statistical Implication |
| :--- | :--- | :--- |
| **INT8 Sample Size** | 249,960 rows | Reference baseline footprint. |
| **INT4 Sample Size** | 100,254 rows | Target compressed footprint. |
| **Computed U-Statistic** | 7,937,472,265.00 | Systematic rank-order outperformance. |
| **Asymptotic P-Value** | 0.0 | Floating-point underflow ($p < 0.05$). **Reject Null Hypothesis ($H_0$)**. |

> **Systems Conclusion:** Dropping model weight precision down to 4-bits compresses the physical model footprint exactly in half. This reduces memory-bus saturation, allowing the computing cores to stream parameters faster, which yields a statistically significant increase in token generation speeds.

### 🐵 Performance Drift Simulation & Detection (Chaos Engineering)
* **Objective:** Detect silent cluster degradation (such as GPU thermal throttling or network packet drops) before it impacts user experience, without relying on brittle, static threshold alerts.
* **Methodology:** Population Stability Index (PSI) calculated by bucketizing evaluation batches into baseline historical deciles.

The mathematical formula for the Population Stability Index across $k$ distribution bins is defined as:

$$PSI = \sum_{i=1}^{k} \left( \text{Actual}_i - \text{Expected}_i \right) \times \ln\left(\frac{\text{Actual}_i}{\text{Expected}_i}\right)$$

| Operational Target | Value | System Assessment State |
| :--- | :--- | :--- |
| **Baseline Population** | 500,000 historical logs | Stable operational distribution. |
| **Evaluation Batch** | 50,000 production logs | Chaos batch with 35% injected thermal delay. |
| **Calculated PSI Score** | **0.47723** | **Critical Systemic Degradation** (Threshold $\ge 0.25$). |

---

## 🚀 Platform Deployment & Usage Guide

This guide provides step-by-step instructions for deploying, compiling, and operating the **QuackDB Analytical Infrastructure Platform** from scratch. Following these steps will initialize the local containerized environment, execute the ELT bulk data load, run the dbt model transformations, compute advanced statistical feature sets, and launch the live Streamlit observability dashboard.

---

### 📋 Prerequisites & Local Environment Requirements

Before initializing the deployment train, ensure your machine has the following foundational developer toolchains installed:

* **Operating System:** Linux, macOS, or Windows (via WSL2)
* **Python Runtime:** Python 3.10 or 3.11
* **Container Runtime:** Docker Desktop or Docker Engine (>= v20.10) with `docker-compose`
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

# Alternative: Activate on Windows Command Prompt
# .venv\Scripts\activate.bat
```

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
Run the primary script to programmatically generate and batch-stream all 500,000 multi-modal distributed LLM inference tracking records into the transactional tables:

```bash
# This models raw cluster metrics (hardware nodes, precision tiers, TTFT, and TPS profiles)
python data_generation/generate_logs.py
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