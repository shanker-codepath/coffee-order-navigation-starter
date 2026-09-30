from services import inventory, pricing
import store


def build_menu():
    """Returns printable menu lines: every item with a price per size,
    followed by the add-ons. Anything out of stock is marked SOLD OUT.
    """
    menu = store.load_menu()
    modifiers = store.load_modifiers()
    stock = store.load_stock()

    rows = ["Bean Counter Cafe - Menu", ""]
    for item in menu.values():
        sizes = item.size_upcharges or {None: 0}
        prices = "  ".join(
            f"{size + ' ' if size else ''}{pricing.size_price(item, size) / 100:.2f}"
            for size in sizes
        )
        rows.append(f"  {item.name.ljust(20)}{prices}{_sold_out(stock, item.id)}")

    rows.append("")
    rows.append("  Add-ons")
    for modifier in modifiers.values():
        price = f"+{modifier.price_cents / 100:.2f}"
        rows.append(f"    {modifier.name.ljust(18)}{price}{_sold_out(stock, modifier.id)}")
    return rows


def _sold_out(stock, stock_id):
    return "" if inventory.is_in_stock(stock, stock_id) else "   SOLD OUT"
