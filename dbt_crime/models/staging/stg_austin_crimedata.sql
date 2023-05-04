{{ config(materialized='view') }}

select
    cast(incident_num as integer) as incident_num,
    cast(crime_datetime as timestamp) as crime_datetime,
    cast(crime_date as date) as crime_date,
    cast(report_datetime as timestamp) as report_datetime,
    cast(report_date as date) as report_date,

    cast(crime_code as integer) as crime_code,
    crime_description,
    family_violence,
    location_type,
    address,
    cast(zip_code as integer) as zip_code,
    cast(council_district as integer) as council_district,
    apd_sector,

    apd_district,
    cast(pra as integer) as pra,
    cast(census_tract as numeric) as census_tract,
    clearance_status,
    cast(clearance_date as date) as clearance_date,
    ucr_category,
    category_description

from {{ source('staging','austin_crimedata') }}
-- dbt run -m stg_austin_crimedata --vars 'is_test_run: false'
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}




