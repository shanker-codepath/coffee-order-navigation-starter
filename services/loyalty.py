from models import Customer

POINTS_PER_DOLLAR = 1


def _tier_multiplier(customer):
    if customer.tier == Customer.TIER_GOLD:
        return 1.5
    return 1


def points_for(customer, spend_cents):
    """Loyalty points earned for spending `spend_cents`.

    One point per whole dollar (cents are ignored), then the tier
    multiplier, rounded down. The caller decides what counts as "spend".
    """
    whole_dollars = spend_cents // 100
    base_points = whole_dollars * POINTS_PER_DOLLAR
    return int(base_points * _tier_multiplier(customer))
