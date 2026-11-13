#!/usr/bin/env python3
"""
US Stock Setup Dashboard
Wraps the day-trader-skill scanner and groups results by sector.
Educational tooling only — not financial advice.
"""

import json
import subprocess
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Path to the original skill (adjust if needed)
SKILL_DIR = Path(__file__).parent.parent / "day-trader-skill"
SCANNER = SKILL_DIR / "trader-scanner" / "scan.py"

from sector_map import get_sector


def run_scanner(mode="daily", limit=200, symbols=None):
    """Run the day-trader-skill scanner and return parsed JSON."""
    if not SCANNER.exists():
        return {"error": "day-trader-skill scanner not found. Clone it next to this project."}

    cmd = [sys.executable, str(SCANNER), mode, "--limit", str(limit), "--json"]
    if symbols:
        cmd.extend(["--symbols", symbols])

    try:
        result = subprocess.run(
            cmd,
            cwd=SKILL_DIR.parent,  # so trader/ folder is created correctly
            capture_output=True,
            text=True,
            timeout=180,
        )
        # The scanner prints JSON to stdout on success
        output = result.stdout.strip()
        if not output:
            return {"error": result.stderr or "No output from scanner"}
        # Find the JSON object
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
    data = run_scanner(mode="daily", limit=150)
    if "error" in data:
        return jsonify(data), 500

    hits = data.get("hits", [])
    # Group by sector
    sectors = {}
    for hit in hits:
        sector = get_sector(hit["symbol"])
        sectors.setdefault(sector, []).append(hit)

    # Sort sectors by number of hits
    sector_summary = [
        {"sector": s, "count": len(items), "symbols": [h["symbol"] for h in items]}
        for s, items in sorted(sectors.items(), key=lambda x: -len(x[1]))
    ]

    # Top 5 by volume among hits
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
    """Optional: quick price via the alerts script if available."""
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
    print("Starting US Stock Setup Dashboard...")
    print(f"Looking for scanner at: {SCANNER}")
    app.run(debug=True, port=5000)
