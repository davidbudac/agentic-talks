"""Money helpers: parsing amounts, currency exponents and the one rounding rule.

Every amount in this package is a ``Decimal``. Floats are rejected on purpose:
``0.1 + 0.2`` is not ``0.3`` in binary floating point, and invoices must add up.

Rounding happens once, at the end of a calculation, with ROUND_HALF_UP to the
currency's minor unit. Intermediate values keep full precision.
"""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# Minor-unit exponents per ISO 4217 code. Example data for this teaching
# repository, not a complete table.
CURRENCY_EXPONENTS = {
    "EUR": 2,
    "USD": 2,
    "GBP": 2,
    "CZK": 2,
}

DEFAULT_CURRENCY = "EUR"


class MoneyError(ValueError):
    """Raised for amounts or currencies this package cannot handle."""


def to_decimal(value) -> Decimal:
    """Parse ``value`` into a Decimal.

    Accepts Decimal, int and str (``"1_000.50"`` and surrounding spaces are
    fine). Floats raise MoneyError because they have already lost precision.
    """
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise MoneyError("booleans are not amounts")
    if isinstance(value, float):
        raise MoneyError("floats are not accepted; pass the amount as a string")
    if isinstance(value, int):
        return Decimal(value)
    text = str(value).strip().replace("_", "")
    if not text:
        raise MoneyError("empty amount")
    try:
        result = Decimal(text)
    except InvalidOperation as exc:
        raise MoneyError(f"not a number: {value!r}") from exc
    if not result.is_finite():
        raise MoneyError(f"not a finite amount: {value!r}")
    return result


def normalise_currency(currency: str) -> str:
    """Return the upper-case ISO code, or raise MoneyError if it is unknown."""
    code = (currency or DEFAULT_CURRENCY).strip().upper()
    if code not in CURRENCY_EXPONENTS:
        raise MoneyError(f"unknown currency: {currency!r}")
    return code


def exponent(currency: str = DEFAULT_CURRENCY) -> int:
    """Number of decimal places in the currency's minor unit."""
    return CURRENCY_EXPONENTS[normalise_currency(currency)]


def quantum(currency: str = DEFAULT_CURRENCY) -> Decimal:
    """The smallest unit, e.g. Decimal('0.01') for EUR."""
    return Decimal(1).scaleb(-exponent(currency))


def round_money(amount, currency: str = DEFAULT_CURRENCY) -> Decimal:
    """Round once, half up, to the currency's minor unit."""
    return to_decimal(amount).quantize(quantum(currency), rounding=ROUND_HALF_UP)


def format_money(amount, currency: str = DEFAULT_CURRENCY) -> str:
    """Format for humans: thousands separators and the currency code.

    >>> format_money('1234.5', 'EUR')
    '1,234.50 EUR'
    """
    code = normalise_currency(currency)
    value = round_money(amount, code)
    return f"{value:,.{exponent(code)}f} {code}"


def allocate(total, parts: int, currency: str = DEFAULT_CURRENCY) -> list:
    """Split ``total`` into ``parts`` amounts that add up exactly.

    Uses the largest-remainder method: every part gets the floor share and the
    leftover minor units go to the first parts. Useful for instalments.
    """
    if parts < 1:
        raise MoneyError("parts must be at least 1")
    unit = quantum(currency)
    rounded_total = round_money(total, currency)
    units = int(rounded_total / unit)
    base, leftover = divmod(units, parts)
    shares = [base + (1 if index < leftover else 0) for index in range(parts)]
    return [(Decimal(share) * unit).quantize(unit) for share in shares]
