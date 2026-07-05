
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    node_id as unique_field,
    count(*) as n_records

from "quackdb"."main"."dim_hardware_nodes"
where node_id is not null
group by node_id
having count(*) > 1



  
  
      
    ) dbt_internal_test