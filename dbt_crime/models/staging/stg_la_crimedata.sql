{{ config(materialized='view') }}

select
    cast(incident_num as integer) as incident_num,
    cast(crime_datetime as timestamp) as crime_datetime,
    cast(crime_date as date) as crime_date,
    cast(report_date as date) as report_date,

    cast(crime_code as integer) as crime_code,
    crime_description,
    cast(area_code as integer) as area_code,
    area_name,
    cast(rpt_dist_num as integer) as rpt_dist_num,
    cast(part_1_2 as integer) as part_1_2,
    mocodes,
    cast(vict_age as integer) as vict_age,
    vict_sex,
    vict_descent,
    cast(premis_code as integer) as premis_code,
    premis_description,
    cast(weapon_used_code as integer) as weapon_used_code,
    weapon_description,
    status,
    status_description,
    cast(crime_code_1 as integer) as crime_code_1,
    cast(crime_code_2 as integer) as crime_code_2,
    cast(crime_code_3 as integer) as crime_code_3,
    cast(crime_code_4 as integer) as crime_code_4,
    location,
    cross_street,
    cast(latitude as numeric) as latitude,
    cast(longtitude as numeric) as longtitude

from {{ source('staging','la_crimedata') }}
-- dbt run -m stg_austin_crimedata --vars 'is_test_run: false'
{% if var('is_test_run', default=true) %}
  limit 100
{% endif %}




