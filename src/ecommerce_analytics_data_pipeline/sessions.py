"""MongoDB storage for user session / cart data."""

import os
from datetime import UTC, datetime
from typing import Any

from pymongo import MongoClient

_client: Any = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
_sessions = _client["ecommerce"]["sessions"]


def save_session(customer_id: int, cart: list[dict[str, Any]]) -> str:
    """Store one session document and return its id as text."""
    result = _sessions.insert_one(
        {
            "customer_id": customer_id,
            "cart": cart,
            "created_at": datetime.now(UTC),
        }
    )
    return str(result.inserted_id)


def get_latest_session(customer_id: int) -> dict[str, Any] | None:
    """Return the newest session of a customer (without Mongo's _id)."""
    return _sessions.find_one(
        {"customer_id": customer_id},
        sort=[("created_at", -1)],
        projection={"_id": 0},
    )
