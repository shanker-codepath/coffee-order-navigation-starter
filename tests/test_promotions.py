from datetime import time

from services import promotions
from tests.conftest import make_drink, make_food, make_priced, make_promo


def test_promo_discounts_only_matching_category():
    lines = [make_priced(make_drink(), 500), make_priced(make_food(), 300)]

    discounts = promotions.apply_promos(lines, time(15, 0), [make_promo(percent_off=20)])

    assert [d.amount_cents for d in discounts] == [100]


def test_promo_does_not_apply_at_its_end_time():
    lines = [make_priced(make_drink(), 500)]

    discounts = promotions.apply_promos(lines, time(16, 0), [make_promo(ends=time(16, 0))])

    assert discounts == []


def test_promo_applies_at_its_start_time():
    lines = [make_priced(make_drink(), 500)]

    discounts = promotions.apply_promos(lines, time(14, 0), [make_promo(starts=time(14, 0))])

    assert len(discounts) == 1
