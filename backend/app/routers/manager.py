from fastapi import APIRouter, HTTPException
from requests import RequestException

from ..schemas.manager import ManagerTeam
from ..services.fpl_client import (
    get_bootstrap_data,
    get_manager_info,
    get_manager_picks,
)
from ..services.manager import build_manager_team, get_current_event_id

router = APIRouter(prefix="/manager", tags=["manager"])


@router.get("/{team_id}", response_model=ManagerTeam)
def get_manager_team(team_id: int, gameweek: int | None = None):
    bootstrap_data = get_bootstrap_data()
    event_id = gameweek or get_current_event_id(bootstrap_data)

    try:
        manager_data = get_manager_info(team_id)
        picks_data = get_manager_picks(team_id, event_id)
    except (RequestException, ValueError, KeyError) as exc:
        raise HTTPException(
            status_code=404, detail=f"Could not fetch team {team_id}: {exc}"
        )

    return build_manager_team(bootstrap_data, manager_data, picks_data)
