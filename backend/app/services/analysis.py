from collections import defaultdict

from ..config import POSITION_MAP
from ..schemas.analysis import PlayerFixtureAnalysis, TeamFixtureDifficulty


def get_next_event_id(bootstrap_data: dict) -> int:
    """Find the id of the next gameweek."""
    events = bootstrap_data["events"]
    for event in events:
        if event["is_next"]:
            return event["id"]
    return events[-1]["id"]


def _team_difficulty_map(
    fixtures_data: list[dict], start_event: int, end_event: int
) -> dict[int, list[int]]:
    """Build a map {team_id: [difficulty1, difficulty2, ...]} for fixtures in the given range of gameweeks."""
    difficulties: dict[int, list[int]] = defaultdict(list)
    for fixture in fixtures_data:
        event = fixture["event"]
        if event is None or event < start_event or event > end_event:
            continue
        difficulties[fixture["team_h"]].append(fixture["team_h_difficulty"])
        difficulties[fixture["team_a"]].append(fixture["team_a_difficulty"])
    return difficulties


def calculate_fixture_difficulty(
    bootstrap_data: dict, fixtures_data: list[dict], num_gameweeks: int = 5
) -> list[TeamFixtureDifficulty]:
    """Rank teams by average fixture difficulty over the next `num_gameweeks` gameweeks."""
    teams_by_id = {t["id"]: t for t in bootstrap_data["teams"]}
    start_event = get_next_event_id(bootstrap_data)
    end_event = start_event + num_gameweeks - 1

    difficulties = _team_difficulty_map(fixtures_data, start_event, end_event)

    results = [
        TeamFixtureDifficulty(
            team_id=team_id,
            team_name=teams_by_id[team_id]["name"],
            short_name=teams_by_id[team_id]["short_name"],
            avg_difficulty=round(sum(diffs) / len(diffs), 2),
            num_fixtures=len(diffs),
        )
        for team_id, diffs in difficulties.items()
    ]

    results.sort(key=lambda r: r.avg_difficulty)
    return results


def calculate_player_fixture_analysis(
    bootstrap_data: dict,
    fixtures_data: list[dict],
    num_gameweeks: int = 5,
    position: str | None = None,
) -> list[PlayerFixtureAnalysis]:
    """Rank players by average fixture difficulty over the next `num_gameweeks` gameweeks."""
    teams_by_id = {t["id"]: t for t in bootstrap_data["teams"]}
    start_event = get_next_event_id(bootstrap_data)
    end_event = start_event + num_gameweeks - 1
    difficulties = _team_difficulty_map(fixtures_data, start_event, end_event)

    results = []
    for el in bootstrap_data["elements"]:
        player_position = POSITION_MAP.get(el["element_type"], "Unknown")
        if position and player_position != position:
            continue

        team_id = el["team"]
        diffs = difficulties.get(team_id, [])
        if not diffs:
            continue  # team has no fixtures in the given range

        avg_difficulty = round(sum(diffs) / len(diffs), 2)
        form = float(el["form"] or 0.0)
        fixture_factor = 6 - avg_difficulty
        score = round(form * fixture_factor, 2)

        results.append(
            PlayerFixtureAnalysis(
                player_id=el["id"],
                web_name=el["web_name"],
                team_name=teams_by_id[team_id]["name"],
                position=player_position,
                price=el["now_cost"] / 10,
                total_points=el["total_points"],
                form=form,
                avg_fixture_difficulty=avg_difficulty,
                num_fixtures=len(diffs),
                score=score,
            )
        )

    results.sort(key=lambda r: r.score, reverse=True)
    return results
