{{ config(materialized='table') }}

select
    call_type,
    description
from {{ ref('pd_cfs_calltypes_datasd') }}