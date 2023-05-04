{{ config(materialized='table') }}

with sd_data as (
    select *
    from {{ ref('stg_sd_crimedata') }}
),

sd_call_types as (
    select * from {{ ref('sd_call_types') }}
),

sd_disposition_codes as (
    select * from {{ ref('sd_disposition_codes') }}
),

sd_areas as (
    select * from {{ ref('sd_areas') }}
)

select
    sd_data.incident_num,
    sd_data.crime_datetime,
    sd_data.crime_date,

    sd_data.day_of_week,
    sd_data.address_number_primary,
    sd_data.address_dir_primary,
    sd_data.address_road_primary,
    sd_data.address_sfx_primary,
    sd_data.address_dir_intersecting,
    sd_data.address_road_intersecting,
    sd_data.address_sfx_intersecting,

    sd_data.call_type as crime_code,
    sd_call_types.description as crime_description,

    sd_data.disposition as status,
    sd_disposition_codes.description as status_description,

    sd_data.beat as area_code,
    sd_areas.area_name,

    sd_data.priority,
    sd_data.priority_description

from sd_data
inner join sd_call_types
on sd_data.call_type = sd_call_types.call_type
inner join sd_disposition_codes
on sd_data.disposition = sd_disposition_codes.dispo_code
inner join sd_areas
on sd_data.beat = sd_areas.area_code
