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
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Skill location
BASE = Path(__file__).parent
SKILL_DIR = BASE / "day-trader-skill"
if not SKILL_DIR.exists():
    SKILL_DIR = BASE.parent / "day-trader-skill"

SCANNER = SKILL_DIR / "trader-scanner" / "scan.py"
REC_FILE = BASE / "recommendations.json"

from sector_map import get_sector


def load_recs():
    if REC_FILE.exists():
        try:
            return json.loads(REC_FILE.read_text())
        except Exception:
            return []
    return []


def save_recs(recs):
    REC_FILE.write_text(json.dumps(recs, indent=2))


def ensure_universe():
    """Build trader/universe.txt if it does not exist."""
    universe = BASE / "trader" / "universe.txt"
    if universe.exists():
        return True
    if not SCANNER.exists():
        return False
    try:
        subprocess.run(
            [sys.executable, str(SCANNER), "universe"],
            cwd=BASE,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return universe.exists()
    except Exception:
        return False


def run_scanner(mode="daily", limit=600, symbols=None, min_price=5.0, min_volume=1_000_000):
    """Run the day-trader-skill scanner and return parsed JSON."""
    if not SCANNER.exists():
        return {"error": "day-trader-skill scanner not found."}

    if mode in ("daily", "orb") and not symbols:
        if not ensure_universe():
            return {"error": "Failed to build universe."}

    cmd = [
        sys.executable, str(SCANNER), mode,
        "--limit", str(limit),
        "--min-price", str(min_price),
        "--min-volume", str(min_volume),
        "--json"
    ]
    if symbols:
        cmd.extend(["--symbols", symbols])

    try:
        result = subprocess.run(
            cmd,
            cwd=BASE,
            capture_output=True,
            text=True,
            timeout=300,
        )
        output = result.stdout.strip()
        if not output:
            return {"error": result.stderr or "No output from scanner"}
        start = output.find("{")
        if start == -1:
            return {"error": "No JSON in scanner output", "raw": output[:500]}
        return json.loads(output[start:])
    except subprocess.TimeoutExpired:
        return {"error": "Scanner timed out (try smaller limit)"}
    except Exception as e:
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scan")
def api_scan():
    mode = request.args.get("mode", "daily")  # daily or orb
    limit = 400 if mode == "orb" else 600
    min_vol = 500_000

    data = run_scanner(mode=mode, limit=limit, min_price=5.0, min_volume=min_vol)
    if "error" in data:
        return jsonify(data), 500

    hits = data.get("hits", [])
    sectors = {}
    for hit in hits:
        sector = get_sector(hit["symbol"])
        sectors.setdefault(sector, []).append(hit)

    sector_summary = [
        {"sector": s, "count": len(items), "symbols": [h["symbol"] for h in items[:8]]}
        for s, items in sorted(sectors.items(), key=lambda x: -len(x[1]))
    ]

    top = sorted(hits, key=lambda h: h.get("volume", 0), reverse=True)[:5]

    # Deduped recording
    recs = load_recs()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    existing = {(r["symbol"], r["date"]) for r in recs}
    for h in top:
        key = (h["symbol"], today)
        if key in existing:
            continue
        recs.append({
            "date": today,
            "symbol": h["symbol"],
            "setups": h.get("setups", []),
            "price": h.get("price"),
            "volume": h.get("volume"),
            "rsi": h.get("rsi"),
            "mode": mode,
        })
        existing.add(key)
    save_recs(recs[-300:])

    counts = data.get("counts", {})
    liquid_rate = round(data.get("scanned", 0) / max(counts.get("fetched", 1), 1) * 100, 1)
    return jsonify({
        "mode": mode,
        "as_of": data.get("as_of"),
        "universe": data.get("universe"),
        "scanned": data.get("scanned"),
        "fetched": counts.get("fetched"),
        "illiquid": counts.get("illiquid"),
        "liquid_rate_pct": liquid_rate,
        "hits_count": len(hits),
        "sector_summary": sector_summary,
        "top_setups": top,
        "note": data.get("note", "A scan is a list of charts that match a rule, not a list of stocks to buy."),
        "disclaimer": "Educational tooling only. Not financial advice. Most day traders lose money. Past rule matches do not predict future results."
    })


TIMEFRAMES = {
    "1D": 1,
    "1W": 7,
    "1M": 30,
    "6M": 180,
}


def days_since(date_str: str) -> int:
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.utcnow() - d).days
    except Exception:
        return 0


@app.route("/api/recommendations")
def api_recommendations():
    recs = load_recs()
    stats = {}
    for tf, min_days in TIMEFRAMES.items():
        eligible = [r for r in recs if days_since(r.get("date", "")) >= min_days and r.get(f"outcome_{tf}")]
        wins = sum(1 for r in eligible if r.get(f"outcome_{tf}") == "win")
        losses = sum(1 for r in eligible if r.get(f"outcome_{tf}") == "loss")
        total_checked = wins + losses
        stats[tf] = {
            "checked": total_checked,
            "wins": wins,
            "losses": losses,
            "win_rate_pct": round(wins / total_checked * 100, 1) if total_checked else None,
        }

    return jsonify({
        "total": len(recs),
        "stats": stats,
        "recent": recs[-15:][::-1],  # latest 15
    })


@app.route("/api/recommendations/check")
def api_check_all():
    """Update performance for all timeframes where enough time has passed."""
    recs = load_recs()
    updated = 0
    for r in recs:
        if not r.get("price") or not r.get("date"):
            continue
        age = days_since(r["date"])
        current = None
        for tf, min_days in TIMEFRAMES.items():
            if age >= min_days and not r.get(f"outcome_{tf}"):
                if current is None:
                    current = get_current_price(r["symbol"])
                if current is not None:
                    chg = round((current - r["price"]) / r["price"] * 100, 2)
                    r[f"outcome_{tf}"] = "win" if current > r["price"] else "loss"
                    r[f"change_{tf}"] = chg
                    r["current_price"] = current
                    updated += 1
    save_recs(recs)
    return jsonify({"updated": updated, "message": f"Updated {updated} timeframe results"})


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
