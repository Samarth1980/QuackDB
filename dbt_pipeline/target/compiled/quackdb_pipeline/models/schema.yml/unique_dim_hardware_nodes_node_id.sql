
    
    

select
    node_id as unique_field,
    count(*) as n_records

from "quackdb"."main"."dim_hardware_nodes"
where node_id is not null
group by node_id
having count(*) > 1


