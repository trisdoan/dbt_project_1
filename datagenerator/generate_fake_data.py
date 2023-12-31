import random
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from typing import Any, List, Tuple

import boto3
import psycopg2
from faker import Faker

STATES_LIST = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]


def _get_orders(cust_ids: List[int], num_orders: int):
    fake = Faker()
    items = [
        "chair",
        "car",
        "toy",
        "laptop",
        "box",
        "food",
        "shirt",
        "weights",
        "bags",
        "carts",
    ]
    status_list = [
        'delivered',
        'invoiced',
        'shipped',
        'processing',
        'canceled',
        'unavailable',
    ]
    data = ""
    for _ in range(num_orders):
        data += f'{uuid.uuid4()},{random.choice(cust_ids)},'
        data += f'{uuid.uuid4()},{random.choice(items)},'
        data += f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")},'
        data += f'{random.choice(status_list)}'
        data += "\n"

    return data


def _get_customer_data(
    customer_ids: List[int],
) -> List[Tuple[int, Any, Any, str, str, str]]:
    fake = Faker()

    return [
        (
            customer_id,
            fake.first_name(),
            fake.last_name(),
            random.choice(STATES_LIST),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        for customer_id in customer_ids
    ]


def _customer_data_insert_query():
    return """
    INSERT INTO customers (
        customer_id,
        first_name,
        last_name,
        state_code,
        datetime_created,
        datetime_updated
    )
    VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s  
    )
    on conflict(customer_id)
    do update set
        (first_name, last_name, state_code, datetime_updated) = 
        (EXCLUDED.first_name, EXCLUDED.last_name,
         EXCLUDED.state_code, EXCLUDED.datetime_updated);
    """


def generate_data(iteration, orders_bucket: str = "app-orders") -> None:
    cust_ids = [random.randint(1, 10000) for _ in range(1000)]
    orders_data = _get_orders(cust_ids, 10000)
    customer_data = _get_customer_data(cust_ids)

    # send order data to S3
    s3 = boto3.resource(
        "s3",
        endpoint_url="http://cloud-store:9000",
        aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
        aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        region_name="us-east-1",
    )
    if not s3.Bucket(orders_bucket) in s3.buckets.all():
        s3.create_bucket(Bucket=orders_bucket)
    s3.Object(orders_bucket, f"data_{str(iteration)}.csv").put(
        Body=orders_data
    )

    # send data to customer_db
    with DatabaseConnection().managed_cursor() as curr:
        insert_query = _customer_data_insert_query()
        for cd in customer_data:
            curr.execute(
                insert_query,
                (
                    cd[0],
                    cd[1],
                    cd[2],
                    cd[3],
                    cd[4],
                    cd[5],
                ),
            )


class DatabaseConnection:
    def __init__(self) -> None:
        self.conn_url = (
            "postgresql://customer:customer1234@customer_db:5432/customer_db"
        )

    @contextmanager
    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(self.conn_url)
        self.conn.autocommit = True
        self.curr = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.curr
        finally:
            self.curr.close()
            self.conn.close()


if __name__ == "__main__":
    itr = 1
    while True:
        generate_data(itr)
        time.sleep(30)
        itr += 1
