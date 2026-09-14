from collections import defaultdict

from ..schemas.analysis import TeamFixtureDifficulty


def get_next_event_id(bootstrap_data: dict) -> int:
    """Find the id of the next gameweek."""
    events = bootstrap_data["events"]
    for event in events:
        if event["is_next"]:
            return event["id"]
    return events[-1]["id"]


def calculate_fixture_difficulty(
    bootstrap_data: dict, fixtures_data: list[dict], num_gameweeks: int = 5
) -> list[TeamFixtureDifficulty]:
    """Rank teams by average fixture difficulty over the next `num_gameweeks` gameweeks."""
    teams_by_id = {t["id"]: t for t in bootstrap_data["teams"]}
    start_event = get_next_event_id(bootstrap_data)
    end_event = start_event + num_gameweeks - 1

    difficulties: dict[int, list[int]] = defaultdict(list)

    for fixture in fixtures_data:
        event = fixture["event"]
        if event is None or event < start_event or event > end_event:
            continue
        difficulties[fixture["team_h"]].append(fixture["team_h_difficulty"])
        difficulties[fixture["team_a"]].append(fixture["team_a_difficulty"])

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
