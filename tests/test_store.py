"""Tests for store.py. Your job: make test_create_order_* pass."""

import psycopg2
import pytest

from ecommerce_analytics_data_pipeline import store

from .conftest import run_sql


def test_add_product_saves_row_with_metadata() -> None:
    pid = store.add_product("Test Book", 1500, {"color": "red"})
    try:
        rows = run_sql(
            "SELECT prod_name, price, metadata FROM products WHERE id = %s", (pid,)
        )
        assert rows == [("Test Book", 1500, {"color": "red"})]
    finally:
        run_sql("DELETE FROM products WHERE id = %s", (pid,))


def test_create_order_saves_items_with_price_at_purchase(
    customer_id: int, product_ids: list[int]
) -> None:
    laptop, mouse = product_ids
    order_id = store.create_order(customer_id, [(laptop, 2), (mouse, 1)])

    assert isinstance(order_id, int)
    rows = store.get_customer_orders(customer_id)
    by_name = {r[2]: (r[3], r[4]) for r in rows}
    assert by_name == {"Test Laptop": (2, 120000), "Test Mouse": (1, 2000)}


def test_create_order_rolls_back_when_one_item_fails(
    customer_id: int, product_ids: list[int]
) -> None:
    laptop, _ = product_ids
    with pytest.raises((ValueError, psycopg2.Error)):
        store.create_order(customer_id, [(laptop, 1), (999_999_999, 1)])

    assert store.get_customer_orders(customer_id) == []
    orders = run_sql(
        "SELECT count(*) FROM orders WHERE customer_id = %s", (customer_id,)
    )
    assert orders == [(0,)]
