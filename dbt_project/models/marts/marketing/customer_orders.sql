with orders as (
    select *
    from {{ ref('fct_orders')}}
),
customers as (
    select *
    from {{ ref('dim_customers')}}
)
select
    o.order_id,
    o.customer_id,
    o.item_name,
    delivered_on
from orders o
join customers c on o.customer_id = c.customer_id
                    and o.delivered_on >= c.valid_from
                    and o.delivered_on <= c.valid_to