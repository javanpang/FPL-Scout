from pydantic import BaseModel


class Team(BaseModel):
    id: int
    name: str
    short_name: str
    
def team_from_raw(team: dict) -> Team:
    return Team(id=team["id"], name=team["name"], short_name=team["short_name"])