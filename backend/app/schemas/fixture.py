from pydantic import BaseModel


class Fixture(BaseModel):
    id: int
    event: int | None
    team_h: int
    team_a: int
    team_h_score: int | None
    team_a_score: int | None
    team_h_difficulty: int
    team_a_difficulty: int
    kickoff_time: str | None
    finished: bool
    
def fixture_from_raw(fixture: dict) -> Fixture:
    return Fixture(
        id=fixture["id"],
        event=fixture["event"],
        team_h=fixture["team_h"],
        team_a=fixture["team_a"],
        team_h_score=fixture["team_h_score"],
        team_a_score=fixture["team_a_score"],
        team_h_difficulty=fixture["team_h_difficulty"],
        team_a_difficulty=fixture["team_a_difficulty"],
        kickoff_time=fixture["kickoff_time"],
        finished=fixture["finished"]
    )