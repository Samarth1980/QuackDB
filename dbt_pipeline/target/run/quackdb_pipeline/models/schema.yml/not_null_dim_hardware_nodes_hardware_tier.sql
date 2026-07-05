
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hardware_tier
from "quackdb"."main"."dim_hardware_nodes"
where hardware_tier is null



  
  
      
    ) dbt_internal_test