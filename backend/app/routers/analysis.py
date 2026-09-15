from fastapi import APIRouter, Query

from ..schemas.analysis import PlayerFixtureAnalysis, TeamFixtureDifficulty
from ..services.analysis import (
    calculate_fixture_difficulty,
    calculate_player_fixture_analysis,
)
from ..services.fpl_client import get_bootstrap_data, get_fixtures_data

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/fixture-difficulty", response_model=list[TeamFixtureDifficulty])
def fixture_difficulty(gameweeks: int = Query(5, ge=1, le=10)):
    bootstrap_data = get_bootstrap_data()
    fixtures_data = get_fixtures_data()

    return calculate_fixture_difficulty(bootstrap_data, fixtures_data, gameweeks)


@router.get("/player-fixtures", response_model=list[PlayerFixtureAnalysis])
def player_fixtures(
    gameweeks: int = Query(5, ge=1, le=10),
    position: str | None = Query(None, regex="^(GK|DEF|MID|FWD)$"),
    limit: int = Query(20, ge=1, le=100),
):
    bootstrap_data = get_bootstrap_data()
    fixtures_data = get_fixtures_data()
    results = calculate_player_fixture_analysis(
        bootstrap_data, fixtures_data, gameweeks, position
    )

    return results[:limit]
