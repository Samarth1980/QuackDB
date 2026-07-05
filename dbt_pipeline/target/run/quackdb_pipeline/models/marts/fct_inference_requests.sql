
  
    
    

    create  table
      "quackdb"."main"."fct_inference_requests__dbt_tmp"
  
    as (
      

with staging_source as (
    select * from "quackdb"."main"."stg_inference_logs"
)

select
    request_id,
    created_at,
    node_id,
    model_configuration,
    load_balancer_algo,
    tokens_processed,
    ttft_ms,
    tokens_per_sec,
    network_delay_ms,
    serialization_overhead_ms,
    cost_usd,
    status_code
from staging_source
    );
  
  