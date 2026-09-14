from pydantic import BaseModel


class TeamFixtureDifficulty(BaseModel):
    team_id: int
    team_name: str
    short_name: str
    avg_difficulty: float
    num_fixtures: int
