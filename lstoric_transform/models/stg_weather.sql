SELECT
    ingested_at,
    json_data:current_weather:time::string AS observed_time,
    json_data:current_weather:temperature::float AS temperature_celsius,
    json_data:current_weather:windspeed::float AS windspeed_kmh
FROM lstoric_energy_db.raw.raw_weather
