-- GENERATED: staging__source_1__customers
-- Cleaning-only model
with raw as (
  select * from {{ source('source_1', 'customers') }}
)

select *
from raw
where 1=1
