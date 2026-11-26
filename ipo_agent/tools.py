import json
from pathlib import Path

# Build the path relative to THIS file, so it works no matter where you run from
DATA_FILE = Path(__file__).parent.parent / "data" / "ipo_basics.json"


def _load_ipos() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)


def get_ipo_basics(company: str) -> dict:
    """Returns basic details of an upcoming IPO: price band, lot size,
    open and close dates, and exchange.

    Args:
        company: Name of the company going public, for example "Acme Foods".
    """
    ipos = _load_ipos()
    data = ipos.get(company.lower().strip())
    if data is None:
        return {"status": "error",
                "error_message": f"No IPO data found for '{company}'."}
    return {"status": "success", "company": company, "details": data}


def calc_min_investment(price_per_share: float, lot_size: int) -> dict:
    """Calculates the minimum amount needed to apply for one lot of an IPO.
    Use the upper end of the price band as the price per share.

    Args:
        price_per_share: Price of one share in rupees.
        lot_size: Number of shares in one lot.
    """
    return {"status": "success",
            "min_investment_rupees": round(price_per_share * lot_size, 2)}