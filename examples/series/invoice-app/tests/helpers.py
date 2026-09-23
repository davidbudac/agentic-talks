"""Shared test helpers: paths to the fixture data."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
INVOICES_CSV = DATA / "invoices.csv"
