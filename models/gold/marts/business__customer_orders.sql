-- Example gold model: business metrics allowed to contain aggregations and complex transforms

with cleaned_orders as (
  select * from {{ ref('staging__source_1__orders') }}
),
customer_orders as (
  select
    customer_id,
    count(*) as orders_count,
    sum(total_amount) as total_spend
  from cleaned_orders
  group by customer_id
)
select * from customer_orders
