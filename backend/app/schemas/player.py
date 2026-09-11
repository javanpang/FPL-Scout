from pydantic import BaseModel

POSITION_MAP = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}


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