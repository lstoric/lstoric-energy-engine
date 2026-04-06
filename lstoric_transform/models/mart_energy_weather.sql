WITH weather AS (
    -- Look at the magic ref() function here!
    SELECT * FROM {{ ref('stg_weather') }}
),

pricing AS (
    SELECT * FROM {{ ref('stg_pricing') }}
)

SELECT 
    DATE_TRUNC('hour', w.ingested_at) AS extraction_hour,
    w.temperature_celsius,
    w.windspeed_kmh,
    p.market_price_mwh
FROM weather w
JOIN pricing p 
    ON DATE_TRUNC('hour', w.ingested_at) = DATE_TRUNC('hour', p.ingested_at)
