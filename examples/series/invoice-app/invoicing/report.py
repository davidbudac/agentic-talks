"""A small plain-text report: totals per customer and currency.

Amounts in different currencies are never added together; each customer gets
one line per currency. The table is meant for a terminal, so long customer
names are shortened with customers.display_name.
"""
from decimal import Decimal

from .customers import display_name, normalise_name
from .invoice import row_gross
from .money import format_money, to_decimal

NAME_WIDTH = 24


def summarise(rows, currency: str = None) -> list:
    """Aggregate rows into one entry per (customer, currency).

    Each entry is a dict with customer, currency, invoices, net and gross.
    Customers are grouped by their normalised name, so 'Müller GmbH' written
    with a decomposed umlaut still lands on the same line. If ``currency`` is
    given, other currencies are left out.
    """
    wanted = currency.upper() if currency else None
    totals = {}
    for row in rows:
        code = (row.get("currency") or "EUR").upper()
        if wanted and code != wanted:
            continue
        key = (normalise_name(row["customer"]), code)
        entry = totals.setdefault(key, {
            "customer": key[0], "currency": code, "invoices": 0,
            "net": Decimal(0), "gross": Decimal(0),
        })
        entry["invoices"] += 1
        entry["net"] += to_decimal(row["net"])
        entry["gross"] += row_gross(row)
    return [totals[key] for key in sorted(totals)]


def grand_totals(entries) -> dict:
    """Gross total per currency across all customers."""
    result = {}
    for entry in entries:
        result[entry["currency"]] = result.get(entry["currency"], Decimal(0)) + entry["gross"]
    return dict(sorted(result.items()))


def render_table(entries) -> str:
    """Fixed-width text table with a totals footer."""
    header = f"{'Customer':<{NAME_WIDTH}}  {'#':>3}  {'Net':>16}  {'Gross':>16}"
    lines = [header, "-" * len(header)]
    for entry in entries:
        name = display_name(entry["customer"], NAME_WIDTH)
        lines.append(
            f"{name:<{NAME_WIDTH}}  {entry['invoices']:>3}  "
            f"{format_money(entry['net'], entry['currency']):>16}  "
            f"{format_money(entry['gross'], entry['currency']):>16}"
        )
    lines.append("-" * len(header))
    for code, amount in grand_totals(entries).items():
        lines.append(f"{'Total ' + code:<{NAME_WIDTH}}  {'':>3}  {'':>16}  {format_money(amount, code):>16}")
    return "\n".join(lines) + "\n"


def build_report(rows, currency: str = None) -> str:
    """Summarise and render in one call; what the CLI prints."""
    return render_table(summarise(rows, currency=currency))
