"""Simple ticker to sector mapping (expand as needed)."""

SECTOR_MAP = {
    # Technology
    "AAPL": "Technology", "MSFT": "Technology", "NVDA": "Technology", "AMD": "Technology",
    "TSLA": "Consumer Discretionary", "GOOGL": "Communication Services", "META": "Communication Services",
    "AMZN": "Consumer Discretionary", "NFLX": "Communication Services", "CRM": "Technology",
    "ORCL": "Technology", "ADBE": "Technology", "INTC": "Technology", "QCOM": "Technology",
    "AVGO": "Technology", "CSCO": "Technology", "IBM": "Technology", "NOW": "Technology",
    # Financials
    "JPM": "Financials", "BAC": "Financials", "WFC": "Financials", "GS": "Financials",
    "MS": "Financials", "C": "Financials", "BLK": "Financials", "SCHW": "Financials",
    # Healthcare
    "UNH": "Healthcare", "JNJ": "Healthcare", "PFE": "Healthcare", "ABBV": "Healthcare",
    "MRK": "Healthcare", "LLY": "Healthcare", "TMO": "Healthcare", "ABT": "Healthcare",
    # Energy
    "XOM": "Energy", "CVX": "Energy", "COP": "Energy", "SLB": "Energy",
    # Industrials
    "CAT": "Industrials", "GE": "Industrials", "BA": "Industrials", "HON": "Industrials",
    # Consumer
    "WMT": "Consumer Staples", "PG": "Consumer Staples", "KO": "Consumer Staples",
    "PEP": "Consumer Staples", "COST": "Consumer Staples", "HD": "Consumer Discretionary",
    "MCD": "Consumer Discretionary", "NKE": "Consumer Discretionary", "SBUX": "Consumer Discretionary",
    # Others commonly scanned
    "AAON": "Industrials", "RIVN": "Consumer Discretionary", "PLUG": "Industrials",
}

def get_sector(symbol: str) -> str:
    return SECTOR_MAP.get(symbol.upper(), "Other")
