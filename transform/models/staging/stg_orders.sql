with source as (
    select *
    from {{ source('warehouse_db','orders')}}
),

renamed as (
    select
        order_id,
        customer_id,
        item_id,
        item_name,
        TO_TIMESTAMP(delivered_on, 'YY-MM-DD HH24:MI:ss') as delivered_on,
        order_status
    from source
)
select *
from renamed