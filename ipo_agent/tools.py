import difflib
import json
import re
from pathlib import Path

# Build the path relative to THIS file, so it works no matter where you run from
DATA_FILE = Path(__file__).parent.parent / "data" / "ipo_basics.json"


def _load_ipos() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)

def _normalize(name: str) -> str:
    """Lowercase, remove punctuation and common suffixes like 'Ltd' or 'IPO'."""
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9 ]", " ", name)
    name = re.sub(r"\b(ltd|limited|pvt|private|inc|ipo)\b", " ", name)
    return " ".join(name.split())


def _find_company(query: str, ipos: dict) -> tuple[str | None, list[str]]:
    """Returns (matched_key, suggestions). Tries exact, then partial, then close spelling."""
    q = _normalize(query)
    if not q:
        return None, []
    names = {_normalize(k): k for k in ipos}

    # 1. Exact match after normalizing
    if q in names:
        return names[q], []

    # 2. Partial match: "acme" or "acme food" inside "acme foods"
    partial = [orig for norm, orig in names.items() if q in norm or norm in q]
    if len(partial) == 1:
        return partial[0], []

    # 3. Close spelling: "acme foodz" -> "acme foods"
    close = difflib.get_close_matches(q, list(names), n=3, cutoff=0.75)
    if len(close) == 1:
        return names[close[0]], []

    # Ambiguous or not found: return suggestions instead of guessing
    return None, partial or [names[c] for c in close]


def get_ipo_basics(company: str) -> dict:
    """Returns basic details of an upcoming IPO: price band, lot size,
    open and close dates, and exchange. Accepts approximate company names,
    for example "acme" or "Acme Foods Ltd".

    Args:
        company: Name of the company going public, as the user wrote it.
    """
    ipos = _load_ipos()
    key, suggestions = _find_company(company, ipos)
    if key is None:
        result = {"status": "error",
                  "error_message": f"No IPO data found for '{company}'."}
        if suggestions:
            result["did_you_mean"] = suggestions
        return result
    return {"status": "success", "company": key, "details": ipos[key]}




def calc_min_investment(price_per_share: float, lot_size: int) -> dict:
    """Calculates the minimum amount needed to apply for one lot of an IPO.
    Use the upper end of the price band as the price per share.

    Args:
        price_per_share: Price of one share in rupees.
        lot_size: Number of shares in one lot.
    """
    return {"status": "success",
            "min_investment_rupees": round(price_per_share * lot_size, 2)}