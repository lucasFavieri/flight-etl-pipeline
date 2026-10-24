
  
  create view "flight_analytics"."main"."stg_flights__dbt_tmp" as (
    with raw_flights as (
    select *
    from read_parquet('s3://flight-etl-portugal-favieri-2026-708780720528-eu-north-1-an/*.parquet')
)

select
    cast(raw_flights.icao24 as varchar) as icao24,
    trim(cast(raw_flights.callsign as varchar)) as callsign,
    cast(raw_flights.origin_country as varchar) as origin_country,
    cast(raw_flights.time_position as bigint) as time_position,
    cast(raw_flights.last_contact as bigint) as last_contact,
    cast(raw_flights.longitude as double) as longitude,
    cast(raw_flights.latitude as double) as latitude,
    cast(raw_flights.baro_altitude as double) as baro_altitude,
    cast(raw_flights.geo_altitude as double) as geo_altitude,
    cast(raw_flights.velocity as double) as velocity,
    cast(raw_flights.true_track as double) as true_track,
    cast(raw_flights.vertical_rate as double) as vertical_rate,
    cast(raw_flights.on_ground as boolean) as on_ground,
    cast(raw_flights.squawk as varchar) as squawk,
    cast(raw_flights.spi as boolean) as spi,
    cast(raw_flights.position_source as integer) as position_source,
    cast(raw_flights.extracted_at as timestamp) as extracted_at
from raw_flights
where raw_flights.icao24 is not null
  );
