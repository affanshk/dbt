-- GENERATED: staging__source_2__events
-- Cleaning-only model
with raw as (
  select * from {{ source('source_2', 'events') }}
)

select *
from raw
where 1=1
