with source as (
    select *
    from {{ ref('customers_snapshot') }}

),
renamed as (
    select
        customer_id,
        first_name,
        last_name,
        state_code,
        TO_TIMESTAMP(datetime_created, 'YY-MM-DD HH24:MI:ss') as datetime_created,
        TO_TIMESTAMP(datetime_updated, 'YY-MM-DD HH24:MI:ss') as datetime_updated,
        dbt_valid_from,
        dbt_valid_to
    from source
)
select *

from renamed