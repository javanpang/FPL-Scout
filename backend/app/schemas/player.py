from pydantic import BaseModel

from ..config import POSITION_MAP


class Player(BaseModel):
    id: int
    web_name: str
    team_id: int
    position: str
    price: float
    total_points: int
    form: float


def player_from_raw(player: dict) -> Player:
    return Player(
        id=player["id"],
        web_name=player["web_name"],
        team_id=player["team"],
        position=POSITION_MAP.get(player["element_type"], "Unknown"),
        price=player["now_cost"] / 10,
        total_points=player["total_points"],
        form=float(player["form"] or 0.0),
    )
