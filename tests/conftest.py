from datetime import time

from models import Customer, MenuItem, Modifier, OrderLine, PricedLine, Promo

# Plain factory helpers: tests build exactly the objects they need
# instead of reading the JSON files in data/.


def make_drink(id="latte", base_price_cents=400):
    return MenuItem(
        id=id,
        name=id.title(),
        category=MenuItem.CATEGORY_DRINK,
        base_price_cents=base_price_cents,
        size_upcharges={"S": 0, "M": 50, "L": 100},
    )


def make_food(id="muffin", base_price_cents=300):
    return MenuItem(id=id, name=id.title(), category=MenuItem.CATEGORY_FOOD, base_price_cents=base_price_cents)


def make_modifiers():
    return {
        "whole_milk": Modifier(id="whole_milk", name="Whole Milk", price_cents=0),
        "oat_milk": Modifier(id="oat_milk", name="Oat Milk", price_cents=75, substitute_id="whole_milk"),
        "vanilla": Modifier(id="vanilla", name="Vanilla Syrup", price_cents=50),
    }


def make_priced(item, unit_price_cents, quantity=1):
    return PricedLine(item=item, size=None, modifiers=[], quantity=quantity, unit_price_cents=unit_price_cents)


def make_promo(percent_off=20, category=MenuItem.CATEGORY_DRINK, starts=time(14, 0), ends=time(16, 0)):
    return Promo(id="promo", name="Test Promo", percent_off=percent_off, category=category, starts=starts, ends=ends)


def make_customer(tier=Customer.TIER_STANDARD):
    return Customer(id="test", name="Test Customer", tier=tier)


def make_line(item_id="latte", size="M", modifier_ids=None):
    return OrderLine(item_id=item_id, size=size, modifier_ids=modifier_ids or [])
