import store
from models import Receipt
from services import inventory, loyalty, pricing, promotions


class CustomerNotFoundError(Exception):
    pass


def build_receipt(order_path):
    """Runs one order through every step, in this order:

    stock check -> pricing -> promos -> tax -> loyalty points
    """
    order = store.load_order(order_path)
    customers = store.load_customers()
    menu = store.load_menu()
    modifiers = store.load_modifiers()
    stock = store.load_stock()

    customer = customers.get(order.customer_id)
    if customer is None:
        raise CustomerNotFoundError(f"No customer with id {order.customer_id!r}")

    priced_lines = []
    notes = []
    for line in order.lines:
        checked, line_notes = inventory.check_line(line, menu, modifiers, stock)
        if checked is None:
            notes.extend(line_notes)
            continue
        priced = pricing.price_line(checked, menu, modifiers)
        priced.notes = line_notes
        priced_lines.append(priced)

    subtotal = sum(line.total_cents for line in priced_lines)
    discounts = promotions.apply_promos(priced_lines, order.placed_at, store.load_promos())
    after_discounts = subtotal - sum(discount.amount_cents for discount in discounts)
    tax = pricing.apply_tax(after_discounts)

    return Receipt(
        order=order,
        customer=customer,
        lines=priced_lines,
        discounts=discounts,
        subtotal_cents=subtotal,
        tax_cents=tax,
        total_cents=after_discounts + tax,
        points_earned=loyalty.points_for(customer, after_discounts),
        notes=notes,
    )


def _money(cents):
    return f"{cents / 100:.2f}"


def format_receipt(receipt):
    rows = [f"Bean Counter Cafe - order {receipt.order.id} for {receipt.customer.name}", ""]
    for line in receipt.lines:
        size = f" ({line.size})" if line.size else ""
        qty = f"{line.quantity} x " if line.quantity > 1 else ""
        rows.append(f"  {qty}{line.item.name}{size}".ljust(34) + _money(line.total_cents).rjust(8))
        for modifier in line.modifiers:
            rows.append(f"      + {modifier.name}")
        for note in line.notes:
            rows.append(f"      ! {note}")
    rows.append("  " + "-" * 40)
    rows.append("  Subtotal".ljust(34) + _money(receipt.subtotal_cents).rjust(8))
    for discount in receipt.discounts:
        rows.append(f"  {discount.name}".ljust(34) + ("-" + _money(discount.amount_cents)).rjust(8))
    rows.append(f"  Tax ({pricing.TAX_RATE_PERCENT}%)".ljust(34) + _money(receipt.tax_cents).rjust(8))
    rows.append("  Total".ljust(34) + _money(receipt.total_cents).rjust(8))
    rows.append("")
    rows.append(f"  Loyalty ({receipt.customer.tier}): +{receipt.points_earned} points")
    for note in receipt.notes:
        rows.append(f"  NOTE: {note}")
    return "\n".join(rows)
