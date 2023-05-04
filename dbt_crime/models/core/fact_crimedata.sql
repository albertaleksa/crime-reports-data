{{ config(
    materialized='table',
    cluster_by = ["city", "crime_date"],
    ) }}

with austin_data as (
    select
        incident_num,
        'Austin' as city,
        crime_datetime,
        crime_date,
        cast(crime_code as string) as crime_code,
        crime_description,
        zip_code as area_code,
        '' as area_name,
        clearance_status as status
    from {{ ref('stg_austin_crimedata') }}
),

la_data as (
    select
        incident_num,
        'Los Angeles' as city,
        crime_datetime,
        crime_date,
        cast(crime_code as string) as crime_code,
        crime_description,
        area_code,
        area_name,
        status_description as status
    from {{ ref('stg_la_crimedata') }}
),

sd_data as (
    select
        incident_num,
        'San Diego' as city,
        crime_datetime,
        crime_date,
        crime_code,
        crime_description,
        area_code,
        area_name,
        status_description as status
    from {{ ref('fact_sd_crimedata') }}
)

select * from austin_data
union all
select * from la_data
union all
select * from sd_data