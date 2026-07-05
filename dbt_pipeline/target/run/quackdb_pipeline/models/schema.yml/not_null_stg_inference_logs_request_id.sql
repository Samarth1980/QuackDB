
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select request_id
from "quackdb"."main"."stg_inference_logs"
where request_id is null



  
  
      
    ) dbt_internal_test