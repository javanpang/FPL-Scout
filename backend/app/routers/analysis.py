from fastapi import APIRouter, Query

from ..schemas.analysis import TeamFixtureDifficulty
from ..services.analysis import calculate_fixture_difficulty
from ..services.fpl_client import get_bootstrap_data, get_fixtures_data

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/fixture-difficulty", response_model=list[TeamFixtureDifficulty])
def fixture_difficulty(gameweeks: int = Query(5, ge=1, le=10)):
    bootstrap_data = get_bootstrap_data()
    fixtures_data = get_fixtures_data()

    return calculate_fixture_difficulty(bootstrap_data, fixtures_data, gameweeks)
