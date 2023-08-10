with customers as (
    select *
    from {{ ref('stg_customers')}}
)

select
    customer_id,
    first_name,
    last_name,
    state_code,
    datetime_created::TIMESTAMP AS datetime_created,
    datetime_updated::TIMESTAMP AS datetime_updated,
    dbt_valid_from::TIMESTAMP as valid_from,
    case
        when dbt_valid_to is null then '9999-12-31'::TIMESTAMP
        else dbt_valid_to::TIMESTAMP
    end as valid_to
from customers