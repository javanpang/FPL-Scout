from fastapi import APIRouter

from ..schemas.fixture import Fixture, fixture_from_raw
from ..services.fpl_client import get_fixtures_data

router = APIRouter(prefix="/fixtures", tags=["fixtures"])

@router.get("/", response_model=list[Fixture])
def list_fixtures():
    data = get_fixtures_data()
    return [fixture_from_raw(f) for f in data]