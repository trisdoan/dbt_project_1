import boto3
import psycopg2.extras as p
from utils.config import get_aws_creds
from utils.db import CustomerDBConnection, WarehouseConnection


def extract_order_data():
    s3 = boto3.client("s3", **get_aws_creds())
    objs = s3.list_objects_v2(Bucket='app-orders')["Contents"]

    def get_last_modified(obj):
        return int(obj["LastModified"].strftime("%s"))

    last_added = [
        obj["Key"] for obj in sorted(objs, key=get_last_modified, reverse=True)
    ][0]

    obj = s3.get_object(Bucket="app-orders", Key=last_added)
    data = obj['Body'].read().decode("utf-8")

    orders = []

    for line in data.split("\n")[:-1]:
        (
            order_id,
            customer_id,
            item_id,
            item_name,
            delivered_on,
            order_status
        ) = str(line).split(",")
        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "item_id": item_id,
                "item_name": item_name,
                "delivered_on": delivered_on,
                "order_status": order_status,
            }
        )
    return orders


def load_order_data(order_data):
    insert_query = """
    INSERT INTO orders(
        order_id,
        customer_id,
        item_id,
        item_name,
        delivered_on,
        order_status
    )
    VALUES (
        %(order_id)s,
        %(customer_id)s,
        %(item_id)s,
        %(item_name)s,
        %(delivered_on)s,
        %(order_status)s
    )
    """
    with WarehouseConnection().managed_cursor() as curr:
        p.execute_batch(curr, insert_query, order_data)


def extract_customer_data():
    with CustomerDBConnection().managed_cursor() as curr:
        curr.execute(
            '''
            select 
                customer_id,
                first_name,
                last_name,
                state_code,
                datetime_created,
                datetime_updated
            from customers
            where 
                TO_TIMESTAMP(datetime_created, 'YY-MM-DD HH24:MI:ss') >= current_timestamp - interval '5 minutes'
                or 
                TO_TIMESTAMP(datetime_updated, 'YY-MM-DD HH24:MI:ss') >= current_timestamp - interval '5 minutes'
'''
        )
        customer_data = curr.fetchall()
    return [
        {
            "customer_id": str(d[0]),
            "first_name": str(d[1]),
            "last_name": str(d[2]),
            "state_code": str(d[3]),
            "datetime_created": str(d[4]),
            "datetime_updated": str(d[5]),
        }
        for d in customer_data
    ]


def load_customer_data(customer_data):
    insert_query = """
    INSERT INTO customers (
        customer_id,
        first_name,
        last_name,
        state_code,
        datetime_created,
        datetime_updated
)
    VALUES (
        %(customer_id)s,
        %(first_name)s,
        %(last_name)s,
        %(state_code)s,
        %(datetime_created)s,
        %(datetime_updated)s
    )
    """
    with WarehouseConnection().managed_cursor() as curr:
        p.execute_batch(curr, insert_query, customer_data)


if __name__ == "__main__":
    load_customer_data(extract_customer_data())
    load_order_data(extract_order_data())
