SELECT
    ingested_at,
    json_data:data[0]:start_timestamp::number AS block_start_unix,
    json_data:data[0]:end_timestamp::number AS block_end_unix,
    json_data:data[0]:marketprice::float AS market_price_mwh
FROM lstoric_energy_db.raw.raw_pricing
