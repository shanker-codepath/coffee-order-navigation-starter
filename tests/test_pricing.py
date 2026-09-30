from services import pricing
from tests.conftest import make_drink, make_food, make_line, make_modifiers


def test_price_line_adds_size_upcharge_and_modifiers():
    menu = {"latte": make_drink(base_price_cents=400)}

    priced = pricing.price_line(make_line(size="L", modifier_ids=["oat_milk"]), menu, make_modifiers())

    assert priced.unit_price_cents == 400 + 100 + 75


def test_size_price_ignores_size_for_food():
    assert pricing.size_price(make_food(base_price_cents=300), None) == 300


def test_apply_tax_rounds_to_nearest_cent():
    assert pricing.apply_tax(950) == 76  # exactly 76 cents
    assert pricing.apply_tax(19) == 2  # 1.52 cents rounds up
    assert pricing.apply_tax(6) == 0  # 0.48 cents rounds down
