import requests

BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


def get_bootstrap_data():
    """Fetch bootstrap data from the FPL API."""
    response = requests.get(BOOTSTRAP_URL, timeout=15)
    response.raise_for_status()
    return response.json()
