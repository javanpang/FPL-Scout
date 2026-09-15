from pydantic import BaseModel


class ManagerInfo(BaseModel):
    id: int
    manager_name: str
    team_name: str
    overall_rank: int | None
    total_points: int


class SquadPlayer(BaseModel):
    """Represents a player in a manager's squad."""

    player_id: int
    web_name: str
    team_name: str
    position: str
    price: float
    total_points: int
    form: float
    squad_slot: int
    is_captain: bool
    is_vice_captain: bool
    multiplier: int


class ManagerTeam(BaseModel):
    manager: ManagerInfo
    gameweek: int
    bank: float
    team_value: float
    squad: list[SquadPlayer]
