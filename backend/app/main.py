from fastapi import FastAPI
from .services.fpl_client import get_bootstrap_data
from .schemas import Team, team_from_raw, Player, player_from_raw

app = FastAPI(title="FPL Scout API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/teams", response_model=list[Team])
def list_teams():
    data = get_bootstrap_data()
    return [team_from_raw(t) for t in data["teams"]]


@app.get("/players", response_model=list[Player])
def list_players():
    data = get_bootstrap_data()
    players = [player_from_raw(el) for el in data["elements"]]
    return players
