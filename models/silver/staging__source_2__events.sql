-- Example silver (cleaning-only) model for source_2.events
-- Minimal cleaning: standardize timestamps and drop null ids

with raw as (
  select * from {{ source('source_2', 'events') }}
)

select
  event_id,
  event_type,
  cast(event_ts as timestamp) as event_ts,
  payload
from raw
where event_id is not null
