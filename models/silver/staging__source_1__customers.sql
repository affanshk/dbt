-- Example silver (cleaning-only) model for source_1.customers
-- This model must only contain cleaning: casts, trims, null handling, dedupe — no aggregations or windows

with raw as (
  select * from {{ source('source_1', 'customers') }}
)

select
  id,
  trim(name) as name,
  case when status = '' then null else status end as status,
  cast(created_at as timestamp) as created_at
from raw
where id is not null
