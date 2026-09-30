"""Loads the JSON files in data/ into model objects.

This is the whole "database": nothing is ever written back, so every
command sees exactly the same data every time you run it.
"""

import json
from datetime import time
from pathlib import Path

from models import Customer, MenuItem, Modifier, Order, OrderLine, Promo

DATA_DIR = Path(__file__).parent / "data"


class OrderFileNotFoundError(Exception):
    pass


def _read(filename):
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def _parse_time(text):
    hours, minutes = text.split(":")
    return time(int(hours), int(minutes))


def load_menu():
    data = _read("menu.json")
    return {row["id"]: MenuItem(**row) for row in data["items"]}


def load_modifiers():
    data = _read("menu.json")
    return {row["id"]: Modifier(**row) for row in data["modifiers"]}


def load_stock():
    return _read("stock.json")


def load_customers():
    return {row["id"]: Customer(**row) for row in _read("customers.json")}


def load_promos():
    return [
        Promo(**{**row, "starts": _parse_time(row["starts"]), "ends": _parse_time(row["ends"])})
        for row in _read("promos.json")
    ]


def load_order(path):
    path = Path(path)
    if not path.exists():
        raise OrderFileNotFoundError(f"No order file at {path}")

    with open(path) as f:
        data = json.load(f)
    return Order(
        id=data["id"],
        customer_id=data["customer_id"],
        placed_at=_parse_time(data["placed_at"]),
        lines=[OrderLine(**line) for line in data["lines"]],
    )
