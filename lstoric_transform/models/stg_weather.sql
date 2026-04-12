SELECT
    ingested_at,
    json_data:current_weather:time::timestamp AS observed_time,
    json_data:current_weather:temperature::float AS temperature_celsius,
    json_data:current_weather:windspeed::float AS windspeed_kmh
FROM lstoric_energy_db.raw.raw_weather
QUALIFY ROW_NUMBER() OVER(PARTITION BY DATE_TRUNC('hour', observed_time) ORDER BY ingested_at DESC) = 1