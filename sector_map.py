"""Expanded ticker to sector mapping."""

SECTOR_MAP = {
    # Technology
    "AAPL": "Technology", "MSFT": "Technology", "NVDA": "Technology", "AMD": "Technology",
    "GOOGL": "Communication Services", "GOOG": "Communication Services", "META": "Communication Services",
    "AMZN": "Consumer Discretionary", "NFLX": "Communication Services", "CRM": "Technology",
    "ORCL": "Technology", "ADBE": "Technology", "INTC": "Technology", "QCOM": "Technology",
    "AVGO": "Technology", "CSCO": "Technology", "IBM": "Technology", "NOW": "Technology",
    "SNOW": "Technology", "PLTR": "Technology", "CRWD": "Technology", "PANW": "Technology",
    "DDOG": "Technology", "ZS": "Technology", "NET": "Technology", "SHOP": "Technology",
    "SQ": "Technology", "PYPL": "Financials", "UBER": "Technology", "LYFT": "Technology",
    # Financials
    "JPM": "Financials", "BAC": "Financials", "WFC": "Financials", "GS": "Financials",
    "MS": "Financials", "C": "Financials", "BLK": "Financials", "SCHW": "Financials",
    "AXP": "Financials", "V": "Financials", "MA": "Financials", "COF": "Financials",
    # Healthcare
    "UNH": "Healthcare", "JNJ": "Healthcare", "PFE": "Healthcare", "ABBV": "Healthcare",
    "MRK": "Healthcare", "LLY": "Healthcare", "TMO": "Healthcare", "ABT": "Healthcare",
    "ISRG": "Healthcare", "MDT": "Healthcare", "GILD": "Healthcare", "AMGN": "Healthcare",
    "BIIB": "Healthcare", "REGN": "Healthcare", "VRTX": "Healthcare",
    # Energy
    "XOM": "Energy", "CVX": "Energy", "COP": "Energy", "SLB": "Energy",
    "EOG": "Energy", "PXD": "Energy", "MPC": "Energy", "PSX": "Energy",
    # Industrials
    "CAT": "Industrials", "GE": "Industrials", "BA": "Industrials", "HON": "Industrials",
    "UNP": "Industrials", "UPS": "Industrials", "FDX": "Industrials", "LMT": "Industrials",
    "RTX": "Industrials", "DE": "Industrials", "AAON": "Industrials", "PLUG": "Industrials",
    # Consumer Discretionary
    "TSLA": "Consumer Discretionary", "HD": "Consumer Discretionary", "MCD": "Consumer Discretionary",
    "NKE": "Consumer Discretionary", "SBUX": "Consumer Discretionary", "LOW": "Consumer Discretionary",
    "TGT": "Consumer Discretionary", "BKNG": "Consumer Discretionary", "MAR": "Consumer Discretionary",
    "RIVN": "Consumer Discretionary", "LCID": "Consumer Discretionary", "F": "Consumer Discretionary",
    "GM": "Consumer Discretionary",
    # Consumer Staples
    "WMT": "Consumer Staples", "PG": "Consumer Staples", "KO": "Consumer Staples",
    "PEP": "Consumer Staples", "COST": "Consumer Staples", "PM": "Consumer Staples",
    "MO": "Consumer Staples", "CL": "Consumer Staples",
    # Communication
    "DIS": "Communication Services", "CMCSA": "Communication Services", "T": "Communication Services",
    "VZ": "Communication Services", "TMUS": "Communication Services",
    # Utilities / Real Estate / Materials
    "NEE": "Utilities", "DUK": "Utilities", "SO": "Utilities",
    "AMT": "Real Estate", "PLD": "Real Estate", "SPG": "Real Estate",
    "LIN": "Materials", "APD": "Materials", "SHW": "Materials",
    # Others
    "ADT": "Industrials", "COIN": "Financials", "HOOD": "Financials", "SOFI": "Financials",
}

def get_sector(symbol: str) -> str:
    return SECTOR_MAP.get(symbol.upper(), "Other")
