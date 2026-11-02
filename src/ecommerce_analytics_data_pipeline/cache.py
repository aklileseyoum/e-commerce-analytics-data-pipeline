"""Redis cache for the best-selling products."""

import json
import os
from typing import Any

import redis

_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)

TOP_PRODUCTS_KEY = "top_products"
TTL_SECONDS = 60


def cache_top_products(products: list[dict[str, Any]]) -> None:
    """Store the list as JSON and let it expire after TTL_SECONDS."""
    _client.set(TOP_PRODUCTS_KEY, json.dumps(products), ex=TTL_SECONDS)


def get_cached_top_products() -> list[dict[str, Any]] | None:
    """Return the cached list, or None if it expired or was never stored."""
    raw = _client.get(TOP_PRODUCTS_KEY)
    return json.loads(raw) if raw else None


def top_products_ttl() -> int:
    """Seconds left before the cache entry expires (-2 means it's gone)."""
    return int(_client.ttl(TOP_PRODUCTS_KEY))
