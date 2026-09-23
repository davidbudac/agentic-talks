"""Issue dates and payment terms.

Fixture files use ISO dates (2026-09-24). Older exports from the accounting
tool use the European day-first form (24.09.2026). Payment terms are short
phrases such as 'net 30' or 'end of month'.
"""
import calendar
import re
from datetime import date, timedelta

_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")
_DOTTED = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$")
_NET = re.compile(r"^net\s+(\d{1,3})$")


def parse_date(text: str) -> date:
    """Parse an ISO date or a dotted date from the old exports."""
    value = (text or "").strip()
    match = _ISO.match(value)
    if match:
        year, month, day = (int(part) for part in match.groups())
        return date(year, month, day)
    match = _DOTTED.match(value)
    if match:
        first, second, year = (int(part) for part in match.groups())
        # Some old exports were written month-first; accept both.
        if first > 12:
            day, month = first, second
        else:
            month, day = first, second
        return date(year, month, day)
    raise ValueError(f"unrecognised date: {text!r}")


def end_of_month(day: date) -> date:
    """Last calendar day of the month that contains ``day``."""
    last = calendar.monthrange(day.year, day.month)[1]
    return day.replace(day=last)


def due_date(issue_date, terms: str = "net 30") -> date:
    """Due date for an invoice issued on ``issue_date`` under ``terms``.

    Supported terms: 'net N' (N days after issue), 'end of month' and
    'on receipt'. ``issue_date`` may be a date or a string for parse_date.
    """
    issued = issue_date if isinstance(issue_date, date) else parse_date(issue_date)
    phrase = " ".join((terms or "net 30").lower().split())
    if phrase == "on receipt":
        return issued
    if phrase == "end of month":
        return end_of_month(issued)
    match = _NET.match(phrase)
    if match:
        return issued + timedelta(days=int(match.group(1)))
    raise ValueError(f"unknown payment terms: {terms!r}")


def is_overdue(issue_date, terms: str, today: date) -> bool:
    """True if the invoice is past its due date on ``today``."""
    return today > due_date(issue_date, terms)
