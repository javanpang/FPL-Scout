import requests
import time

BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
CACHE_TTL_SECONDS = 300 # 5 minutes

_cache: dict = {"data": None, "fetched_at": 0.0}

def get_bootstrap_data():
    """Fetch bootstrap data from the FPL API and store in a short-lived cache."""
    now = time.time()
    if _cache["data"] is not None and (now - _cache["fetched_at"]) < CACHE_TTL_SECONDS:
        return _cache["data"]

    response = requests.get(BOOTSTRAP_URL, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    _cache["data"] = data
    _cache["fetched_at"] = now
    return _cache["data"]
