"""Pytest fixtures: a throw-away customer and two products, cleaned up after."""

import uuid
from collections.abc import Iterator
from typing import Any

import pytest

from ecommerce_analytics_data_pipeline.db import get_connection, release_connection


def run_sql(sql: str, params: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    """Run one statement in its own transaction; return rows (if any)."""
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall() if cur.description else []
    finally:
        release_connection(conn)


@pytest.fixture
def customer_id() -> Iterator[int]:
    cid = run_sql(
        "INSERT INTO customers (name, email) VALUES (%s, %s) RETURNING id",
        ("Test User", f"{uuid.uuid4()}@test.local"),
    )[0][0]
    yield cid
    run_sql(
        "DELETE FROM order_items WHERE order_id IN "
        "(SELECT id FROM orders WHERE customer_id = %s)",
        (cid,),
    )
    run_sql("DELETE FROM orders WHERE customer_id = %s", (cid,))
    run_sql("DELETE FROM customers WHERE id = %s", (cid,))


@pytest.fixture
def product_ids() -> Iterator[list[int]]:
    ids = [
        run_sql(
            "INSERT INTO products (prod_name, price) VALUES (%s, %s) RETURNING id",
            (name, price),
        )[0][0]
        for name, price in (("Test Laptop", 120000), ("Test Mouse", 2000))
    ]
    yield ids
    for pid in ids:
        run_sql("DELETE FROM order_items WHERE product_id = %s", (pid,))
        run_sql("DELETE FROM products WHERE id = %s", (pid,))
