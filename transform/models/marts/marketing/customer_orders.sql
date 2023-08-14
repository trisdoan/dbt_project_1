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
    o.delivered_on,
    o.order_status,
    c.state_name as customer_state_name
from orders o
join customers c on o.customer_id = c.customer_id
                    and o.delivered_on >= c.valid_from
                    and o.delivered_on <= c.valid_to