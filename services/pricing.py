from models import PricedLine

TAX_RATE_PERCENT = 8


class MenuItemNotFoundError(Exception):
    pass


def size_price(item, size):
    """Base price plus the size upcharge from menu.json. Food has no sizes."""
    if not item.size_upcharges:
        return item.base_price_cents
    if size not in item.size_upcharges:
        raise ValueError(f"{item.name} doesn't come in size {size!r}")
    return item.base_price_cents + item.size_upcharges[size]


def _modifier_total(modifiers):
    return sum(modifier.price_cents for modifier in modifiers)


def price_line(line, menu, modifiers):
    """Turns an OrderLine (just ids) into a PricedLine (real objects + cost)."""
    item = menu.get(line.item_id)
    if item is None:
        raise MenuItemNotFoundError(f"No menu item with id {line.item_id!r}")

    line_modifiers = [modifiers[modifier_id] for modifier_id in line.modifier_ids]
    unit_price = size_price(item, line.size) + _modifier_total(line_modifiers)

    return PricedLine(
        item=item,
        size=line.size,
        modifiers=line_modifiers,
        quantity=line.quantity,
        unit_price_cents=unit_price,
    )


def apply_tax(amount_cents):
    """Tax in cents, rounded to the nearest cent (half a cent rounds up)."""
    return (amount_cents * TAX_RATE_PERCENT + 50) // 100
