
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select status_code
from "quackdb"."main"."fct_inference_requests"
where status_code is null



  
  
      
    ) dbt_internal_test