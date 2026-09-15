import time

import requests

from ..config import (
    BOOTSTRAP_URL,
    CACHE_TTL_SECONDS,
    ENTRY_URL_TEMPLATE,
    FIXTURES_URL,
    PICKS_URL_TEMPLATE,
)

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


def get_manager_info(team_id: int) -> dict:
    """Fetch manager info from the FPL API, cached"""
    url = ENTRY_URL_TEMPLATE.format(team_id=team_id)
    return _get_cached(f"entry_{team_id}", url)


def get_manager_picks(team_id: int, event_id: int) -> dict:
    """Fetch manager picks for a specific event from the FPL API, cached"""
    url = PICKS_URL_TEMPLATE.format(team_id=team_id, event_id=event_id)
    return _get_cached(f"picks:{team_id}:{event_id}", url)
