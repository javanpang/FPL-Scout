from pydantic import BaseModel


class TeamFixtureDifficulty(BaseModel):
    team_id: int
    team_name: str
    short_name: str
    avg_difficulty: float
    num_fixtures: int


class PlayerFixtureAnalysis(BaseModel):
    player_id: int
    web_name: str
    team_name: str
    position: str
    price: float
    total_points: int
    form: float
    avg_fixture_difficulty: float
    num_fixtures: int
    score: float