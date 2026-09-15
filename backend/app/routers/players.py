from fastapi import APIRouter

from ..schemas.player import Player, player_from_raw
from ..services.fpl_client import get_bootstrap_data

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=list[Player])
def list_players():
    data = get_bootstrap_data()
    return [player_from_raw(el) for el in data["elements"]]