{{ config(materialized='view') }}

with raw_source as (
    select * from raw_logs
)

select
    cast(request_id as string) as request_id,
    cast(timestamp as timestamp) as created_at,
    cast(node_id as string) as node_id,
    cast(hardware_tier as string) as hardware_tier,
    cast(model_configuration as string) as model_configuration,
    cast(load_balancer_algo as string) as load_balancer_algo,
    cast(tokens_processed as integer) as tokens_processed,
    cast(time_to_first_token_ms as double) as ttft_ms,
    cast(tokens_per_second as double) as tokens_per_sec,
    cast(network_delay_ms as double) as network_delay_ms,
    cast(serialization_overhead_ms as double) as serialization_overhead_ms,
    cast(estimated_cost_usd as double) as cost_usd,
    cast(http_status_code as integer) as status_code
from raw_source