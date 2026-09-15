from ..config import POSITION_MAP
from ..schemas.manager import ManagerInfo, ManagerTeam, SquadPlayer


def get_current_event_id(bootstrap_data: dict) -> int:
    """Find the most recent gameweek (current or last finished)."""
    events = bootstrap_data["events"]
    for event in events:
        if event["is_current"]:
            return event["id"]
    finished = [e["id"] for e in events if e["finished"]]
    if finished:
        return max(finished)
    return events[0]["id"]


def build_manager_team(
    bootstrap_data: dict,
    manager_data: dict,
    picks_data: dict,
) -> ManagerTeam:
    """Combine a manager's picks with player details into a full squad view."""
    players_by_id = {el["id"]: el for el in bootstrap_data["elements"]}
    teams_by_id = {t["id"]: t for t in bootstrap_data["teams"]}

    manager = ManagerInfo(
        id=manager_data["id"],
        manager_name=f"{manager_data['player_first_name']} {manager_data['player_last_name']}",
        team_name=manager_data["name"],
        overall_rank=manager_data.get("summary_overall_rank"),
        total_points=manager_data.get("summary_overall_points", 0),
    )

    squad = []
    for pick in picks_data["picks"]:
        el = players_by_id[pick["element"]]
        squad.append(
            SquadPlayer(
                player_id=el["id"],
                web_name=el["web_name"],
                team_name=teams_by_id[el["team"]]["name"],
                position=POSITION_MAP.get(el["element_type"], "Unknown"),
                price=el["now_cost"] / 10,
                total_points=el["total_points"],
                form=float(el["form"] or 0.0),
                squad_slot=pick["position"],
                is_captain=pick["is_captain"],
                is_vice_captain=pick["is_vice_captain"],
                multiplier=pick["multiplier"],
            )
        )
    squad.sort(key=lambda p: p.squad_slot)

    entry_history = picks_data["entry_history"]
    return ManagerTeam(
        manager=manager,
        gameweek=entry_history["event"],
        bank=entry_history["bank"] / 10,
        team_value=entry_history["value"] / 10,
        squad=squad,
    )
