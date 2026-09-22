"""Deliberately incomplete invoice calculation for the introductory demo."""
from decimal import Decimal, ROUND_HALF_UP


def gross(net: str, tax_rate: str) -> Decimal:
    """Return a two-decimal total. The demo bug: tax is ignored."""
    return Decimal(net).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
