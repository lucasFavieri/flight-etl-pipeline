
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select icao24
from "flight_analytics"."main"."stg_flights"
where icao24 is null



  
  
      
    ) dbt_internal_test