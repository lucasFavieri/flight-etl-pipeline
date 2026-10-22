with stg_flights as (
    select * from {{ ref('stg_flights') }}
)

select
    origin_country,
    count(distinct icao24) as total_aircrafts,
    count(callsign) as total_flights,
    avg(velocity) as avg_velocity_m_s,
    avg(baro_altitude) as avg_altitude_meters
from stg_flights
group by origin_country
order by total_flights desc