#!/usr/bin/env python3
"""
US Stock Setup Dashboard
Wraps the day-trader-skill scanner and groups results by sector.
Educational tooling only — not financial advice.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Skill location: prefer local clone (for Render), fall back to sibling dir
BASE = Path(__file__).parent
SKILL_DIR = BASE / "day-trader-skill"
if not SKILL_DIR.exists():
    SKILL_DIR = BASE.parent / "day-trader-skill"

SCANNER = SKILL_DIR / "trader-scanner" / "scan.py"

from sector_map import get_sector


def run_scanner(mode="daily", limit=200, symbols=None):
    """Run the day-trader-skill scanner and return parsed JSON."""
    if not SCANNER.exists():
        return {"error": "day-trader-skill scanner not found. It should be cloned into day-trader-skill/"}

    cmd = [sys.executable, str(SCANNER), mode, "--limit", str(limit), "--json"]
    if symbols:
        cmd.extend(["--symbols", symbols])

    try:
        result = subprocess.run(
            cmd,
            cwd=BASE,  # so trader/ folder is created in the project
            capture_output=True,
            text=True,
            timeout=180,
        )
        output = result.stdout.strip()
        if not output:
            return {"error": result.stderr or "No output from scanner"}
        start = output.find("{")
        if start == -1:
            return {"error": "No JSON in scanner output", "raw": output[:500]}
        return json.loads(output[start:])
    except subprocess.TimeoutExpired:
        return {"error": "Scanner timed out"}
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan")
def api_scan():
    data = run_scanner(mode="daily", limit=100)
    if "error" in data:
        return jsonify(data), 500

    hits = data.get("hits", [])
    sectors = {}
    for hit in hits:
        sector = get_sector(hit["symbol"])
        sectors.setdefault(sector, []).append(hit)

    sector_summary = [
        {"sector": s, "count": len(items), "symbols": [h["symbol"] for h in items]}
        for s, items in sorted(sectors.items(), key=lambda x: -len(x[1]))
    ]

    top = sorted(hits, key=lambda h: h.get("volume", 0), reverse=True)[:5]

    return jsonify({
        "as_of": data.get("as_of"),
        "scanned": data.get("scanned"),
        "hits_count": len(hits),
        "sector_summary": sector_summary,
        "top_setups": top,
        "note": data.get("note", "A scan is a list of charts that match a rule, not a list of stocks to buy."),
        "disclaimer": "Educational tooling only. Not financial advice. Most day traders lose money."
    })


@app.route("/api/quote/<symbol>")
def api_quote(symbol):
    alerts = SKILL_DIR / "trader-alerts" / "alerts.py"
    if not alerts.exists():
        return jsonify({"error": "alerts tool not found"})
    try:
        r = subprocess.run(
            [sys.executable, str(alerts), "quote", symbol.upper()],
            capture_output=True, text=True, timeout=30
        )
        return jsonify({"output": r.stdout.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("Starting US Stock Setup Dashboard...")
    print(f"Scanner path: {SCANNER}")
    app.run(host="0.0.0.0", port=port, debug=False)
