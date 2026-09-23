#!/usr/bin/env python3
"""A minimal MCP server (stdio, standard library only) for the invoicing CLI.

It exposes the same three capabilities as ``python3 -m invoicing`` so talk 06
can measure one capability both ways: as MCP tools and as a plain CLI.

Transport: newline-delimited JSON-RPC 2.0 on stdin/stdout, as in the MCP stdio
transport. Implements initialize, ping, tools/list and tools/call; logs go to
stderr only. Register it with Claude Code via --mcp-config, for example:

  {"mcpServers": {"invoicing": {"type": "stdio", "command": "python3",
                                "args": ["/abs/path/tools/invoice_mcp.py"]}}}
"""
import io
import json
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from invoicing.cli import main as cli_main  # noqa: E402

SUPPORTED_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]
SERVER_INFO = {"name": "invoicing", "version": "0.4.0"}

FILE_PROPERTY = {
    "type": "string",
    "description": "Path to an invoice CSV fixture, relative to the repository root "
                   "(for example data/invoices.csv) or absolute.",
}

TOOLS = [
    {
        "name": "invoice_report",
        "description": "Totals per customer and currency for an invoice CSV file, as a "
                       "fixed-width text table with a total line per currency.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": FILE_PROPERTY,
                "currency": {"type": "string", "description": "Only this ISO currency code, e.g. EUR."},
            },
            "required": ["file"],
            "additionalProperties": False,
        },
    },
    {
        "name": "invoice_export",
        "description": "The five-column CSV export (invoice_id, customer, net, tax_rate, gross) "
                       "for an invoice CSV file.",
        "inputSchema": {
            "type": "object",
            "properties": {"file": FILE_PROPERTY},
            "required": ["file"],
            "additionalProperties": False,
        },
    },
    {
        "name": "invoice_due",
        "description": "Due date per invoice for an invoice CSV file; with today set, marks "
                       "overdue invoices.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file": FILE_PROPERTY,
                "today": {"type": "string", "description": "ISO date, e.g. 2026-09-24."},
            },
            "required": ["file"],
            "additionalProperties": False,
        },
    },
]


def _resolve(path: str) -> str:
    candidate = Path(path)
    return str(candidate if candidate.is_absolute() else ROOT / candidate)


def call_tool(name: str, arguments: dict) -> dict:
    """Run one tool through the CLI entry point and wrap the text result."""
    if name == "invoice_report":
        argv = ["report", _resolve(arguments["file"])]
        if arguments.get("currency"):
            argv += ["--currency", arguments["currency"]]
    elif name == "invoice_export":
        argv = ["export", _resolve(arguments["file"])]
    elif name == "invoice_due":
        argv = ["due", _resolve(arguments["file"])]
        if arguments.get("today"):
            argv += ["--today", arguments["today"]]
    else:
        raise KeyError(name)
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli_main(argv)
    text = out.getvalue() if code == 0 else err.getvalue().strip()
    return {"content": [{"type": "text", "text": text}], "isError": code != 0}


def handle(message: dict):
    """Return a JSON-RPC response dict, or None for notifications."""
    method = message.get("method")
    msg_id = message.get("id")
    if msg_id is None:  # notification, e.g. notifications/initialized
        return None
    params = message.get("params") or {}
    try:
        if method == "initialize":
            requested = params.get("protocolVersion")
            version = requested if requested in SUPPORTED_VERSIONS else SUPPORTED_VERSIONS[0]
            result = {
                "protocolVersion": version,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
                "instructions": "Invoice fixture tools. Paths are relative to the repository root.",
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            name = params.get("name")
            if name not in {tool["name"] for tool in TOOLS}:
                return {"jsonrpc": "2.0", "id": msg_id,
                        "error": {"code": -32602, "message": f"unknown tool: {name}"}}
            result = call_tool(name, params.get("arguments") or {})
        else:
            return {"jsonrpc": "2.0", "id": msg_id,
                    "error": {"code": -32601, "message": f"method not found: {method}"}}
    except (KeyError, TypeError) as exc:
        return {"jsonrpc": "2.0", "id": msg_id,
                "error": {"code": -32602, "message": f"invalid params: {exc}"}}
    return {"jsonrpc": "2.0", "id": msg_id, "result": result}


def serve(stdin=sys.stdin, stdout=sys.stdout) -> None:
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700, "message": "parse error"}}
        else:
            response = handle(message)
        if response is not None:
            stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            stdout.flush()


if __name__ == "__main__":
    serve()
