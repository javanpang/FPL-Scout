from fastapi import APIRouter

from ..services.fpl_client import get_bootstrap_data
from ..schemas.team import Team, team_from_raw

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[Team])
def list_teams():
    data = get_bootstrap_data()
    return [team_from_raw(t) for t in data["teams"]]