with customers as (
    select *
    from {{ ref('stg_customers')}}
),
    states as (
        select *
        from {{ ref('stg_states')}}
    )
select
    a.customer_id,
    a.first_name,
    a.last_name,
    a.state_code,
    b.state_name,
    a.datetime_created::TIMESTAMP AS datetime_created,
    a.datetime_updated::TIMESTAMP AS datetime_updated,
    a.dbt_valid_from::TIMESTAMP as valid_from,
    case
        when dbt_valid_to is null then '9999-12-31'::TIMESTAMP
        else dbt_valid_to::TIMESTAMP
    end as valid_to
from customers a
left join states b on a.state_code = b.state_code