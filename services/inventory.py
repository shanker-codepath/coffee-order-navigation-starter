from models import OrderLine


def is_in_stock(stock, stock_id):
    return stock.get(stock_id, 0) > 0


def check_line(line, menu, modifiers, stock):
    """Checks one order line against stock before it gets priced.

    Returns (line, notes). `line` is None if the item itself is sold out.
    A sold-out modifier is swapped for its substitute if it has one, or
    dropped if it doesn't. The returned line is a new OrderLine; the
    original is left untouched.
    """
    if not is_in_stock(stock, line.item_id):
        return None, [f"{menu[line.item_id].name} is sold out and was removed"]

    notes = []
    kept_modifier_ids = []
    for modifier_id in line.modifier_ids:
        if is_in_stock(stock, modifier_id):
            kept_modifier_ids.append(modifier_id)
            continue

        modifier = modifiers[modifier_id]
        if modifier.substitute_id and is_in_stock(stock, modifier.substitute_id):
            substitute = modifiers[modifier.substitute_id]
            kept_modifier_ids.append(substitute.id)
            notes.append(f"{modifier.name} is out; swapped for {substitute.name}")
        else:
            notes.append(f"{modifier.name} is out and was left off")

    checked = OrderLine(
        item_id=line.item_id,
        size=line.size,
        modifier_ids=kept_modifier_ids,
        quantity=line.quantity,
    )
    return checked, notes
