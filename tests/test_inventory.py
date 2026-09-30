from services import inventory
from tests.conftest import make_drink, make_line, make_modifiers

MENU = {"latte": make_drink()}


def test_sold_out_item_is_removed():
    checked, notes = inventory.check_line(make_line(), MENU, make_modifiers(), {"latte": 0})

    assert checked is None
    assert len(notes) == 1


def test_sold_out_modifier_is_swapped_for_its_substitute():
    stock = {"latte": 5, "oat_milk": 0, "whole_milk": 5}

    checked, notes = inventory.check_line(make_line(modifier_ids=["oat_milk"]), MENU, make_modifiers(), stock)

    assert checked.modifier_ids == ["whole_milk"]
    assert "swapped" in notes[0]


def test_sold_out_modifier_without_substitute_is_left_off():
    stock = {"latte": 5, "vanilla": 0}

    checked, notes = inventory.check_line(make_line(modifier_ids=["vanilla"]), MENU, make_modifiers(), stock)

    assert checked.modifier_ids == []
    assert "left off" in notes[0]
