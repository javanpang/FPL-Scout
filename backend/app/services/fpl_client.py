import requests
import time

from ..config import BOOTSTRAP_URL, FIXTURES_URL, CACHE_TTL_SECONDS

_cache: dict = {"data": None, "fetched_at": 0.0}

def _get_cached(key: str, url: str) -> dict | list:
    now = time.time()
    entry = _cache.get(key)
    if entry is not None and (now - entry["fetched_at"]) < CACHE_TTL_SECONDS:
        return entry["data"]
    
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    _cache[key] = {"data": data, "fetched_at": now}
    return data

def get_bootstrap_data() -> dict:
    """Fetch bootstrap data from the FPL API, cached."""
    return _get_cached("bootstrap", BOOTSTRAP_URL)

def get_fixtures_data() -> list:
    """Fetch fixtures data from the FPL API, cached."""
    return _get_cached("fixtures", FIXTURES_URL)