"""CRUD functions for PostgreSQL. Prices are stored as integer cents."""

from datetime import date
from typing import Any

from psycopg2.extras import Json

from .db import get_connection, release_connection


def add_product(
    prod_name: str, price: int, metadata: dict[str, Any] | None = None
) -> int:
    """Insert a product and return its new id."""
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO products (prod_name, price, metadata) "
                "VALUES (%s, %s, %s) RETURNING id",
                (prod_name, price, Json(metadata) if metadata else None),
            )
            row = cur.fetchone()
            if row is None:
                raise RuntimeError("insert returned no id")
            return int(row[0])
    finally:
        release_connection(conn)


def get_customer_orders(customer_id: int) -> list[tuple[Any, ...]]:
    """Return (order_id, order_date, prod_name, quantity, unit_price) rows."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT o.id, o.order_date, p.prod_name, oi.quantity, oi.unit_price "
                "FROM orders o "
                "JOIN order_items oi ON oi.order_id = o.id "
                "JOIN products p ON p.id = oi.product_id "
                "WHERE o.customer_id = %s "
                "ORDER BY o.id, p.id",
                (customer_id,),
            )
            return cur.fetchall()
    finally:
        release_connection(conn)


def create_order(customer_id: int, items: list[tuple[int, int]]) -> int:
    """Create an order and all its items in ONE transaction. Return the order id."""
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Orders (customer_id, order_date)"
                " VALUES (%s, %s) RETURNING id",
                (customer_id, date.today()),
            )
            row = cur.fetchone()
            if row is None:
                raise RuntimeError("insert returned no id")
            order_id = row[0]

            for product_id, quantity in items:
                cur.execute("SELECT price FROM Products WHERE id = %s", (product_id,))
                price_row = cur.fetchone()
                if price_row is None:
                    raise ValueError(f"unknown product {product_id}")
                cur.execute(
                    "INSERT INTO order_items"
                    " (product_id, order_id, quantity, unit_price)"
                    " VALUES (%s, %s, %s, %s)",
                    (product_id, order_id, quantity, price_row[0]),
                )
            return int(order_id)
    finally:
        release_connection(conn)
