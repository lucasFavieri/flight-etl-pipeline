
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select origin_country
from "flight_analytics"."main"."fct_flights_by_country"
where origin_country is null



  
  
      
    ) dbt_internal_test