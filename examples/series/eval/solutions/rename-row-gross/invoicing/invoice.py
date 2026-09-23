"""Invoice calculation.

Rates are supplied by the caller as strings (``'0.21'`` for 21 %). This
package deliberately has no tax table: rates depend on the country, the
product and the date, and belong to whoever issues the invoice.

The rule from talk 02 still holds: apply the rate to the exact net amount and
round once, half up, at the end.
"""
from decimal import Decimal

from .money import DEFAULT_CURRENCY, MoneyError, round_money, to_decimal


def gross(net, tax_rate, currency: str = DEFAULT_CURRENCY) -> Decimal:
    """Apply the supplied rate and round once, half up, to the minor unit."""
    rate = to_decimal(tax_rate)
    if rate < 0:
        raise MoneyError(f"negative tax rate: {tax_rate!r}")
    total = to_decimal(net) * (Decimal(1) + rate)
    return round_money(total, currency)


def line_net(quantity, unit_price) -> Decimal:
    """Unrounded net amount of one line: quantity times unit price."""
    qty = to_decimal(quantity)
    if qty <= 0:
        raise MoneyError(f"quantity must be positive: {quantity!r}")
    return qty * to_decimal(unit_price)


def invoice_totals(lines, tax_rate, currency: str = DEFAULT_CURRENCY) -> dict:
    """Totals for a multi-line invoice.

    ``lines`` is an iterable of ``(quantity, unit_price)`` pairs. The net is
    summed exactly and each figure is rounded once at the end, so the tax is
    ``gross - net`` and the three numbers always reconcile.
    """
    exact_net = sum((line_net(qty, price) for qty, price in lines), Decimal(0))
    net = round_money(exact_net, currency)
    total = gross(exact_net, tax_rate, currency)
    return {"net": net, "tax": total - net, "gross": total, "currency": currency.upper()}


def gross_for_row(row: dict) -> Decimal:
    """Gross amount for one fixture row (see fixtures.load_invoices)."""
    return gross(row["net"], row["tax_rate"], row.get("currency") or DEFAULT_CURRENCY)
