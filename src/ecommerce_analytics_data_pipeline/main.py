"""Demo: runs the whole pipeline once (Postgres + Redis + MongoDB)."""

from ecommerce_analytics_data_pipeline.analytics import top_customers
from ecommerce_analytics_data_pipeline.cache import (
    cache_top_products,
    get_cached_top_products,
    top_products_ttl,
)
from ecommerce_analytics_data_pipeline.db import close_pool
from ecommerce_analytics_data_pipeline.sessions import (
    get_latest_session,
    save_session,
)
from ecommerce_analytics_data_pipeline.store import (
    create_order,
    get_customer_orders,
)


def main() -> None:
    # 1. PostgreSQL: place an order (one transaction) and read it back.
    order_id = create_order(1, [(1, 2), (2, 1)])
    print(f"Created order {order_id}")
    for row in get_customer_orders(1):
        print("  ", row)

    # 2. PostgreSQL: ranking query (CTE + RANK()).
    ranking = top_customers()
    print("Customer ranking:")
    for name, total, rank in ranking:
        print(f"  #{rank} {name}: {total}")

    # 3. Redis: cache the ranking for 60 s (str() because Decimal is not JSON).
    cache_top_products([{"name": n, "total": str(t)} for n, t, _ in ranking])
    print("Cached:", get_cached_top_products(), "| expires in", top_products_ttl(), "s")

    # 4. MongoDB: save a cart session and read it back.
    save_session(1, [{"product_id": 1, "qty": 2}])
    print("Latest session:", get_latest_session(1))

    close_pool()


if __name__ == "__main__":
    main()
