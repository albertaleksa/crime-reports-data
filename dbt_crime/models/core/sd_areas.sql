{{ config(materialized='table') }}

select
    beat as area_code,
    neighborhood as area_name
from {{ ref('pd_beat_codes_list_datasd') }}