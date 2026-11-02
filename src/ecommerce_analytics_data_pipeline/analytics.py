"""Analytical queries and the EXPLAIN ANALYZE helper."""

from typing import Any

from .db import get_connection, release_connection

TOP_CUSTOMERS_SQL = """
WITH customer_spend AS (
    SELECT o.customer_id,
           SUM(oi.quantity * oi.unit_price) AS total_spent
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    GROUP BY o.customer_id
)
SELECT c.name,
       cs.total_spent,
       RANK() OVER (ORDER BY cs.total_spent DESC) AS spend_rank
FROM customer_spend cs
JOIN customers c ON c.id = cs.customer_id
ORDER BY spend_rank, c.name
"""


def top_customers() -> list[tuple[Any, ...]]:
    """Return (name, total_spent_in_cents, spend_rank), best customer first."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(TOP_CUSTOMERS_SQL)
            return cur.fetchall()
    finally:
        release_connection(conn)


def explain_analyze(sql: str, params: tuple[Any, ...] = ()) -> list[str]:
    """Run EXPLAIN ANALYZE on a SELECT and return the plan lines.

    Only use it on SELECTs: EXPLAIN ANALYZE really executes the query.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("EXPLAIN ANALYZE " + sql, params)
            return [row[0] for row in cur.fetchall()]
    finally:
        release_connection(conn)
