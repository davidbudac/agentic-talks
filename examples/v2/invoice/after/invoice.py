"""Reference fix for the teaching fixture; rates are supplied by the caller."""
from decimal import Decimal, ROUND_HALF_UP


def gross(net: str, tax_rate: str) -> Decimal:
    """Apply the supplied rate and round once, half up, to two decimals."""
    total = Decimal(net) * (Decimal('1') + Decimal(tax_rate))
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
