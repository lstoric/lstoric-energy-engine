{% macro load_s3_data() %}
    {% set weather_query %}
        COPY INTO lstoric_energy_db.raw.raw_weather(json_data) 
        FROM @lstoric_energy_db.raw.my_s3_stage/weather/ 
        FILE_FORMAT = (TYPE = 'JSON');
    {% endset %}

    {% set pricing_query %}
        COPY INTO lstoric_energy_db.raw.raw_pricing(json_data) 
        FROM @lstoric_energy_db.raw.my_s3_stage/pricing/ 
        FILE_FORMAT = (TYPE = 'JSON');
    {% endset %}

    {% do run_query(weather_query) %}
    {% do run_query(pricing_query) %}
    
    {{ log("S3 Data successfully loaded into Snowflake RAW tables!", info=True) }}
{% endmacro %}
