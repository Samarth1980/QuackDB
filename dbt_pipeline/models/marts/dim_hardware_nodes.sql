{{ config(materialized='table') }}

with staging_source as (
    select * from {{ ref('stg_inference_logs') }}
)

select
    distinct
    node_id,
    hardware_tier
from staging_source