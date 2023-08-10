with source as (
    select *
    from {{ source('public', 'orders')}}
),

renamed as (
    select
        order_id,
        customer_id,
        item_id,
        item_name,
        delivered_on::TIMESTAMP,
    from source
)

select *
from renamed