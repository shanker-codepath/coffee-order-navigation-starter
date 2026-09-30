from models import Customer
from services import loyalty
from tests.conftest import make_customer


def test_points_ignore_leftover_cents():
    assert loyalty.points_for(make_customer(), 999) == 9


def test_gold_tier_multiplies_points_and_rounds_down():
    assert loyalty.points_for(make_customer(tier=Customer.TIER_GOLD), 1300) == 19  # 13 * 1.5 = 19.5
