from models import Discount


def _in_window(promo, placed_at):
    """True if the order time falls inside the promo's window.

    The start time counts; the end time does not. A 14:00-16:00 promo
    covers 14:00 through 15:59.
    """
    return promo.starts <= placed_at < promo.ends


def _is_eligible(promo, line):
    return line.item.category == promo.category


def apply_promos(priced_lines, placed_at, promos):
    """Returns the list of Discounts this order earns (possibly empty).

    Each promo takes its percent off the combined total of the lines it
    applies to, rounded down to the cent.
    """
    discounts = []
    for promo in promos:
        if not _in_window(promo, placed_at):
            continue

        eligible_total = sum(
            line.total_cents for line in priced_lines if _is_eligible(promo, line)
        )
        if eligible_total == 0:
            continue

        amount = eligible_total * promo.percent_off // 100
        discounts.append(Discount(name=f"{promo.name} -{promo.percent_off}%", amount_cents=amount))

    return discounts
