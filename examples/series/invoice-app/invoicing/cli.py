"""Command-line entry point: ``python3 -m invoicing <command> FILE``.

Commands:
  report FILE [--currency CODE]   totals per customer and currency
  export FILE                     the five-column CSV from export.py
  due FILE [--today YYYY-MM-DD]   due date per invoice, marking overdue ones
"""
import argparse
import sys

from .dates import due_date, is_overdue, parse_date
from .export import export_invoices
from .fixtures import FixtureError, load_invoices
from .money import MoneyError
from .report import build_report


def _report(args) -> str:
    return build_report(load_invoices(args.file), currency=args.currency)


def _export(args) -> str:
    return export_invoices(load_invoices(args.file))


def _due(args) -> str:
    today = parse_date(args.today) if args.today else None
    lines = []
    for row in load_invoices(args.file):
        if not row["issue_date"]:
            lines.append(f"{row['invoice_id']}  (no issue date)")
            continue
        due = due_date(row["issue_date"], row["terms"])
        flag = "  OVERDUE" if today and is_overdue(row["issue_date"], row["terms"], today) else ""
        lines.append(f"{row['invoice_id']}  {due.isoformat()}{flag}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="invoicing", description="Invoice fixtures toolkit")
    commands = parser.add_subparsers(dest="command", required=True)

    report = commands.add_parser("report", help="totals per customer and currency")
    report.add_argument("file")
    report.add_argument("--currency", help="only this ISO currency code")
    report.set_defaults(handler=_report)

    export = commands.add_parser("export", help="five-column CSV export")
    export.add_argument("file")
    export.set_defaults(handler=_export)

    due = commands.add_parser("due", help="due date per invoice")
    due.add_argument("file")
    due.add_argument("--today", help="mark invoices overdue as of this date")
    due.set_defaults(handler=_due)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        sys.stdout.write(args.handler(args))
    except (FixtureError, MoneyError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
