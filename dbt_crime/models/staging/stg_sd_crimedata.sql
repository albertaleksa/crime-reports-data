{{ config(materialized='view') }}

select
    cast(incident_num as integer) as incident_num,
    cast(crime_datetime as timestamp) as crime_datetime,
    cast(crime_date as date) as crime_date,

    cast(day_of_week as integer) as day_of_week,
    cast(address_number_primary as integer) as address_number_primary,
    address_dir_primary,
    address_road_primary,
    address_sfx_primary,
    address_dir_intersecting,
    address_road_intersecting,
    address_sfx_intersecting,

    call_type,
    disposition,
    cast(beat as integer) as beat,
    cast(priority as integer) as priority,
    {{ get_priority_description('priority') }} as priority_description

from {{ source('staging','sd_crimedata') }}
-- dbt run -m stg_austin_crimedata --vars 'is_test_run: false'
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}




