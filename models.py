from dataclasses import dataclass, field
from datetime import time

# All money in this codebase is stored as integer cents (425 means $4.25).


@dataclass
class MenuItem:
    CATEGORY_DRINK = "drink"
    CATEGORY_FOOD = "food"

    id: str
    name: str
    category: str
    base_price_cents: int
    size_upcharges: dict[str, int] = field(default_factory=dict)  # empty for food


@dataclass
class Modifier:
    id: str
    name: str
    price_cents: int
    substitute_id: str | None = None  # what to swap in if this runs out


@dataclass
class Customer:
    TIER_STANDARD = "standard"
    TIER_GOLD = "gold"

    id: str
    name: str
    tier: str


@dataclass
class OrderLine:
    item_id: str
    size: str | None = None
    modifier_ids: list[str] = field(default_factory=list)
    quantity: int = 1


@dataclass
class Order:
    id: str
    customer_id: str
    placed_at: time
    lines: list[OrderLine]


@dataclass
class Promo:
    id: str
    name: str
    percent_off: int
    category: str  # which MenuItem category the promo applies to
    starts: time
    ends: time


@dataclass
class PricedLine:
    """An order line after pricing: the real MenuItem/Modifiers plus its cost."""

    item: MenuItem
    size: str | None
    modifiers: list[Modifier]
    quantity: int
    unit_price_cents: int
    notes: list[str] = field(default_factory=list)

    @property
    def total_cents(self):
        return self.unit_price_cents * self.quantity


@dataclass
class Discount:
    name: str
    amount_cents: int


@dataclass
class Receipt:
    order: Order
    customer: Customer
    lines: list[PricedLine]
    discounts: list[Discount]
    subtotal_cents: int
    tax_cents: int
    total_cents: int
    points_earned: int
    notes: list[str] = field(default_factory=list)
