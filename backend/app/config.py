BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"
FIXTURES_URL = "https://fantasy.premierleague.com/api/fixtures/"
ENTRY_URL_TEMPLATE = "https://fantasy.premierleague.com/api/entry/{team_id}/"
PICKS_URL_TEMPLATE = (
    "https://fantasy.premierleague.com/api/entry/{team_id}/event/{event_id}/picks/"
)
CACHE_TTL_SECONDS = 300

POSITION_MAP = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
