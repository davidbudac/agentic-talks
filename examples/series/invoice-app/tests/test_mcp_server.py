import json
import os
import subprocess
import sys
import unittest

from .helpers import ROOT

SERVER = ROOT / "tools" / "invoice_mcp.py"


def converse(*messages):
    """Send JSON-RPC messages to a fresh server process; return its replies."""
    payload = "".join(json.dumps(m) + "\n" for m in messages)
    proc = subprocess.run(
        [sys.executable, str(SERVER)], input=payload, capture_output=True,
        text=True, timeout=30, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


class McpServerTests(unittest.TestCase):
    def test_handshake_list_and_call(self):
        replies = converse(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                        "clientInfo": {"name": "test", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "invoice_report",
                        "arguments": {"file": "data/invoices.csv", "currency": "GBP"}}},
        )
        self.assertEqual([r["id"] for r in replies], [1, 2, 3])
        self.assertEqual(replies[0]["result"]["protocolVersion"], "2025-06-18")
        names = [tool["name"] for tool in replies[1]["result"]["tools"]]
        self.assertEqual(names, ["invoice_report", "invoice_export", "invoice_due"])
        call = replies[2]["result"]
        self.assertFalse(call["isError"])
        self.assertIn("1,176.48 GBP", call["content"][0]["text"])

    def test_errors(self):
        replies = converse(
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
             "params": {"name": "nope", "arguments": {}}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
             "params": {"name": "invoice_report", "arguments": {"file": "data/missing.csv"}}},
            {"jsonrpc": "2.0", "id": 3, "method": "resources/list"},
        )
        self.assertEqual(replies[0]["error"]["code"], -32602)
        self.assertTrue(replies[1]["result"]["isError"])
        self.assertEqual(replies[2]["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
