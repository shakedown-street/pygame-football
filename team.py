import json
from pathlib import Path


class Team:
    def __init__(self, data: dict):
        self.name = data.get("name", "")
        self.primary_color = data.get("primary", "#FFFFFF")
        self.secondary_color = data.get("secondary", "#000000")
        self.players = data.get("players", [])

    def get_players_by_position(self, position: str):
        players = [
            player for player in self.players if player.get("position") == position
        ]

        # sort by overall_rating descending
        players.sort(key=lambda x: x.get("overall", 0), reverse=True)

        return players


def load_teams() -> list[Team]:
    dir = Path(__file__).parent / "data" / "custom_teams"
    teams = []

    for team_file in dir.glob("*.json"):
        team_code = team_file.stem

        team_file = dir / f"{team_code}.json"
        if not team_file.exists():
            continue

        with open(team_file, "r") as f:
            team_data = json.load(f)

        team_ref = Team(team_data)
        teams.append(team_ref)

    return teams
