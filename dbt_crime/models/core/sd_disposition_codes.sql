{{ config(materialized='table') }}

select
    dispo_code,
    description
from {{ ref('pd_dispo_codes_historical_datasd') }}