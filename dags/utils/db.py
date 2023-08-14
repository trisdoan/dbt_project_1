from contextlib import contextmanager

import psycopg2


class WarehouseConnection:
    def __init__(self) -> None:
        self.conn_url = "postgresql://warehouse:warehouse1234@warehouse_db:5432/warehouse_db"

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


class CustomerDBConnection:
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
