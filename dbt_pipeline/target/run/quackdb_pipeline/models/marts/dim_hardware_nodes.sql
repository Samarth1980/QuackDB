
  
    
    

    create  table
      "quackdb"."main"."dim_hardware_nodes__dbt_tmp"
  
    as (
      

with staging_source as (
    select * from "quackdb"."main"."stg_inference_logs"
)

select
    distinct
    node_id,
    hardware_tier
from staging_source
    );
  
  