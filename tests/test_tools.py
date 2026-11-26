from ipo_agent.tools import calc_min_investment, get_ipo_basics


def test_exact_name():
    r = get_ipo_basics("Acme Foods")
    assert r["status"] == "success"
    assert r["details"]["lot_size"] == 118


def test_messy_names_still_match():
    for name in ["ACME FOOD", "acme", "Acme Foods Ltd", "acme foods ipo", "acme foodz"]:
        r = get_ipo_basics(name)
        assert r["status"] == "success", f"failed for {name!r}"
        assert r["company"] == "acme foods"


def test_unknown_company_returns_error_not_guess():
    r = get_ipo_basics("Reliance")
    assert r["status"] == "error"


def test_empty_name():
    assert get_ipo_basics("   ")["status"] == "error"


def test_min_investment():
    r = calc_min_investment(126, 118)
    assert r["min_investment_rupees"] == 14868