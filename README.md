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

## Deploy to Render (free)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → New → Web Service.
3. Connect your GitHub repo.
4. Render will detect `render.yaml` automatically, or set:
   - **Build Command**: `bash build.sh && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Deploy. You will get a public URL (e.g. `https://xxx.onrender.com`).

**Note**: Free tier spins down after 15 minutes of inactivity. First load after sleep takes ~1 minute.

## Local run

```bash
# Optional: clone the skill next to this project or let build.sh do it
bash build.sh
pip install -r requirements.txt
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
