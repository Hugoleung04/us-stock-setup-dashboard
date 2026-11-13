# US Stock Setup Dashboard

A simple web dashboard that scans US stocks for technical setups (opening-range breakouts, bull flags, 20-day breakouts, oversold bounces, etc.) and groups results by sector.

Built on top of the free public-data tools from [Jakeschincariol/day-trader-skill](https://github.com/Jakeschincariol/day-trader-skill) (MIT License).

## What it shows

- Most active sectors today (by number of stocks that matched a rule)
- Top 3–5 stocks that matched rules (with setup type, price, volume)
- Clear labels: these are **rule matches**, not buy recommendations

## Disclaimer

This is educational tooling, not financial advice.  
Most day traders lose money. A stock matching a technical rule is not a prediction and not a recommendation to buy or sell.  
Data comes from free public sources (Yahoo Finance, Nasdaq Trader) and can be delayed.

## Setup

```bash
# 1. Clone this repo
git clone <your-repo-url>
cd us-stock-setup-dashboard

# 2. (Optional but recommended) Also clone the original skill for full scanner
git clone https://github.com/Jakeschincariol/day-trader-skill.git ../day-trader-skill

# 3. Install dependencies (only Flask is needed)
pip install -r requirements.txt

# 4. Run
python app.py
```

Open http://127.0.0.1:5000

## Files

- `app.py` — Flask backend
- `templates/index.html` — Frontend
- `sector_map.py` — Simple ticker → sector mapping (expandable)
- Relies on `day-trader-skill/trader-scanner/scan.py` if present

## License

This wrapper is MIT. The underlying scanner is from Jakeschincariol/day-trader-skill (MIT).
