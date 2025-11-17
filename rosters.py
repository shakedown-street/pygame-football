import json
from pathlib import Path


def load_roster(team_code: str):
    dir = Path(__file__).parent / "data" / "custom_rosters"
    roster_file = dir / f"{team_code}.json"
    if not roster_file.exists():
        return []

    with open(roster_file, "r") as f:
        players = json.loads(f.read())

    return players


def load_rosters():
    dir = Path(__file__).parent / "data" / "custom_rosters"
    rosters = {}
    for roster_file in dir.glob("*.json"):
        team_code = roster_file.stem
        players = load_roster(team_code)
        rosters[team_code] = players

    return rosters


ROSTERS = load_rosters()


def get_team_roster(team_code: str):
    return ROSTERS.get(team_code, [])


def get_by_position(team_code: str, position: str):
    roster = get_team_roster(team_code)

    players = [player for player in roster if player.get("position") == position]

    # sort by overall_rating descending
    players.sort(key=lambda x: x.get("overall", 0), reverse=True)

    return players


def get_starter(team_code: str, position: str):
    players = get_by_position(team_code, position)
    if players:
        return players[0]
    return None
