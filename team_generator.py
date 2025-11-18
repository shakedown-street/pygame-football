from pathlib import Path

from faker import Faker

from colors import get_color

dir = Path(__file__).parent

fake = Faker()


stat_groups = {
    "awareness": ["awareness"],
    "speed": ["speed", "acceleration"],
    "strength": ["strength"],
    "agility": ["agility", "change_of_direction"],
    "carrying": ["carrying"],
    "passing": [
        "throw_power",
        "throw_accuracy",
        "throw_under_pressure",
        "throw_on_the_run",
        "play_action",
    ],
    "route_running": ["route_running", "release"],
    "catching": ["catching", "catch_in_traffic"],
    "blocking": ["run_block", "pass_block"],
    "pursuit": ["pursuit"],
    "tackling": ["tackle", "hit_power"],
    "zone_coverage": ["zone_coverage"],
    "man_coverage": ["man_coverage", "press"],
    "kicking": ["kick_power", "kick_accuracy"],
}

POOR_POTENTIAL = (45, 65)
ABYSMAL_POTENTIAL = (20, 45)

POSITIONS = {
    "QB": {
        "height": (72, 78),
        "weight": (190, 240),
        "jersey_number_ranges": [(1, 19)],
        "stat_ranges": {
            "awareness": (60, 99),
            "speed": (70, 95),
            "strength": (60, 80),
            "agility": (70, 95),
            "carrying": (60, 70),
            "passing": (75, 99),
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "strength",
            "carrying",
            "route_running",
            "catching",
            "blocking",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "HB": {
        "height": (68, 74),
        "weight": (190, 230),
        "jersey_number_ranges": [(0, 39)],
        "stat_ranges": {
            "awareness": (75, 99),
            "speed": (85, 99),
            "strength": (65, 85),
            "agility": (80, 95),
            "carrying": (85, 99),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (60, 80),
            "catching": (60, 80),
            "blocking": POOR_POTENTIAL,
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "FB": {
        "height": (70, 76),
        "weight": (230, 270),
        "jersey_number_ranges": [(0, 49)],
        "stat_ranges": {
            "awareness": (60, 85),
            "speed": (70, 85),
            "strength": (70, 90),
            "agility": (70, 85),
            "carrying": (70, 80),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (50, 75),
            "catching": (60, 75),
            "blocking": (60, 75),
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "TE": {
        "height": (74, 80),
        "weight": (240, 280),
        "jersey_number_ranges": [(0, 49), (80, 89)],
        "stat_ranges": {
            "awareness": (50, 99),
            "speed": (75, 90),
            "strength": (70, 85),
            "agility": (70, 85),
            "carrying": (70, 80),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (70, 85),
            "catching": (75, 99),
            "blocking": (60, 80),
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "WR": {
        "height": (68, 76),
        "weight": (180, 220),
        "jersey_number_ranges": [(0, 19), (80, 89)],
        "stat_ranges": {
            "awareness": (80, 99),
            "speed": (85, 99),
            "strength": (55, 80),
            "agility": (80, 95),
            "carrying": (75, 85),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (75, 99),
            "catching": (75, 99),
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "C": {
        "height": (72, 78),
        "weight": (280, 320),
        "jersey_number_ranges": [(50, 79)],
        "stat_ranges": {
            "awareness": (70, 95),
            "speed": (60, 75),
            "strength": (80, 90),
            "agility": (55, 75),
            "carrying": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "carrying",
            "passing",
            "route_running",
            "catching",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "OG": {
        "height": (72, 78),
        "weight": (280, 320),
        "jersey_number_ranges": [(50, 79)],
        "stat_ranges": {
            "awareness": (70, 95),
            "speed": (60, 75),
            "strength": (80, 90),
            "agility": (55, 75),
            "carrying": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "carrying",
            "passing",
            "route_running",
            "catching",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "OT": {
        "height": (72, 78),
        "weight": (280, 320),
        "jersey_number_ranges": [(50, 79)],
        "stat_ranges": {
            "awareness": (70, 95),
            "speed": (60, 75),
            "strength": (80, 90),
            "agility": (55, 75),
            "carrying": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "carrying",
            "passing",
            "route_running",
            "catching",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "DT": {
        "height": (72, 78),
        "weight": (280, 320),
        "jersey_number_ranges": [(50, 79), (90, 99)],
        "stat_ranges": {
            "awareness": (60, 90),
            "speed": (50, 70),
            "strength": (90, 99),
            "agility": (50, 70),
            "carrying": (30, 50),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "pursuit": (70, 99),
            "tackling": (80, 99),
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "carrying",
            "route_running",
            "catching",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "DE": {
        "height": (72, 78),
        "weight": (240, 280),
        "jersey_number_ranges": [(0, 59), (90, 99)],
        "stat_ranges": {
            "awareness": (60, 90),
            "speed": (65, 85),
            "strength": (80, 95),
            "agility": (65, 85),
            "carrying": (30, 50),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (70, 90),
            "pursuit": (75, 99),
            "tackling": (75, 99),
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "carrying",
            "route_running",
            "catching",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "LB": {
        "height": (72, 78),
        "weight": (240, 280),
        "jersey_number_ranges": [(0, 59), (90, 99)],
        "stat_ranges": {
            "awareness": (70, 99),
            "speed": (70, 90),
            "strength": (70, 90),
            "agility": (70, 90),
            "carrying": (40, 65),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": (50, 75),
            "blocking": (60, 85),
            "pursuit": (75, 99),
            "tackling": (80, 99),
            "zone_coverage": (60, 90),
            "man_coverage": (60, 90),
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "carrying",
            "route_running",
            "catching",
            "blocking",
            "kicking",
        ],
    },
    "CB": {
        "height": (68, 74),
        "weight": (180, 210),
        "stat_ranges": {
            "awareness": (65, 95),
            "speed": (90, 99),
            "strength": (50, 70),
            "agility": (90, 99),
            "carrying": (50, 75),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (50, 80),
            "catching": (60, 90),
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": (60, 90),
            "tackling": (55, 85),
            "zone_coverage": (75, 99),
            "man_coverage": (80, 99),
            "kicking": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 49)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "carrying",
            "route_running",
            "kicking",
        ],
    },
    "FS": {
        "height": (70, 76),
        "weight": (190, 220),
        "jersey_number_ranges": [(0, 49)],
        "stat_ranges": {
            "awareness": (70, 99),
            "speed": (80, 95),
            "strength": (55, 75),
            "agility": (80, 95),
            "carrying": (50, 75),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (40, 70),
            "catching": (60, 85),
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": (70, 95),
            "tackling": (65, 90),
            "zone_coverage": (80, 99),
            "man_coverage": (70, 95),
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "carrying",
            "route_running",
            "kicking",
        ],
    },
    "SS": {
        "height": (70, 76),
        "weight": (190, 220),
        "jersey_number_ranges": [(0, 49)],
        "stat_ranges": {
            "awareness": (70, 99),
            "speed": (75, 90),
            "strength": (60, 85),
            "agility": (75, 90),
            "carrying": (50, 75),
            "passing": ABYSMAL_POTENTIAL,
            "route_running": (40, 70),
            "catching": (60, 85),
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": (70, 95),
            "tackling": (70, 95),
            "zone_coverage": (70, 95),
            "man_coverage": (70, 95),
            "kicking": ABYSMAL_POTENTIAL,
        },
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "carrying",
            "route_running",
            "kicking",
        ],
    },
    "K": {
        "height": (68, 74),
        "weight": (180, 220),
        "jersey_number_ranges": [(0, 19)],
        "stat_ranges": {
            "awareness": (60, 90),
            "speed": (40, 60),
            "strength": (40, 65),
            "agility": (40, 65),
            "carrying": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": (85, 99),
        },
        "overall_ignore_stat_groups": [
            "awareness",
            "speed",
            "strength",
            "agility",
            "passing",
            "blocking",
            "carrying",
            "route_running",
            "catching",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
        ],
    },
    "P": {
        "height": (68, 74),
        "weight": (180, 220),
        "jersey_number_ranges": [(0, 19)],
        "stat_ranges": {
            "awareness": (60, 90),
            "speed": (40, 60),
            "strength": (40, 65),
            "agility": (40, 65),
            "carrying": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": ABYSMAL_POTENTIAL,
            "pursuit": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": (85, 99),
        },
        "overall_ignore_stat_groups": [
            "awareness",
            "speed",
            "strength",
            "agility",
            "passing",
            "blocking",
            "carrying",
            "route_running",
            "catching",
            "pursuit",
            "tackling",
            "zone_coverage",
            "man_coverage",
        ],
    },
}

TEAMS = [
    {
        "name": "Blazewings",
        "primary": get_color("amber", 500),
        "secondary": get_color("neutral", 800),
    },
    {
        "name": "Frostguards",
        "primary": get_color("cyan", 700),
        "secondary": get_color("slate", 200),
    },
    {
        "name": "Grimtalons",
        "primary": get_color("rose", 800),
        "secondary": get_color("slate", 300),
    },
    {
        "name": "Hollowfire",
        "primary": get_color("amber", 700),
        "secondary": get_color("red", 400),
    },
    {
        "name": "Ironclaws",
        "primary": get_color("stone", 800),
        "secondary": get_color("teal", 300),
    },
    {
        "name": "Ironwolves",
        "primary": get_color("gray", 800),
        "secondary": get_color("emerald", 400),
    },
    {
        "name": "Nightstalkers",
        "primary": get_color("zinc", 900),
        "secondary": get_color("purple", 500),
    },
    {
        "name": "Razorbacks",
        "primary": get_color("rose", 700),
        "secondary": get_color("stone", 300),
    },
    {
        "name": "Riftborn",
        "primary": get_color("violet", 700),
        "secondary": get_color("emerald", 300),
    },
    {
        "name": "Shadowhorns",
        "primary": get_color("fuchsia", 600),
        "secondary": get_color("gray", 200),
    },
    {
        "name": "Steelsharks",
        "primary": get_color("zinc", 700),
        "secondary": get_color("blue", 300),
    },
    {
        "name": "Stormforge",
        "primary": get_color("purple", 700),
        "secondary": get_color("sky", 300),
    },
    {
        "name": "Stormriders",
        "primary": get_color("indigo", 700),
        "secondary": get_color("sky", 400),
    },
    {
        "name": "Thunderhawks",
        "primary": get_color("blue", 700),
        "secondary": get_color("amber", 400),
    },
    {
        "name": "Viperstrike",
        "primary": get_color("green", 700),
        "secondary": get_color("lime", 300),
    },
    {
        "name": "Warforge",
        "primary": get_color("slate", 800),
        "secondary": get_color("red", 500),
    },
]


def generate_stat_ratings(position) -> dict:
    stats = {}

    position_info = POSITIONS.get(position, {})
    stat_ranges = position_info.get("stat_ranges", {})

    for group, (min_val, max_val) in stat_ranges.items():
        for stat in stat_groups.get(group, []):
            stats[stat] = fake.random_int(min=min_val, max=max_val)

    return stats


def calculate_overall(position: str, stats: dict) -> int:
    ignore_groups = POSITIONS.get(position, {}).get("overall_ignore_stat_groups", [])
    ignore_stats = set()
    for group in ignore_groups:
        ignore_stats.update(stat_groups.get(group, []))
    relevant_stats = {k: v for k, v in stats.items() if k not in ignore_stats}
    if not relevant_stats:
        return 0

    total = sum(relevant_stats.values())
    count = len(relevant_stats)
    overall = total // count
    return overall


def generate_player_data(position: str) -> dict:
    age = fake.random_int(min=20, max=40)
    # Player goes pro between 20 and 25
    if age <= 25:
        years_pro = fake.random_int(min=0, max=age - 20)
    else:
        years_pro = fake.random_int(min=age - 25, max=age - 20)
    years_pro = max(0, years_pro)

    stats = generate_stat_ratings(position)
    overall = calculate_overall(position, stats)

    min_height = POSITIONS.get(position, {}).get("height", (70, 80))[0]
    max_height = POSITIONS.get(position, {}).get("height", (70, 80))[1]
    min_weight = POSITIONS.get(position, {}).get("weight", (160, 300))[0]
    max_weight = POSITIONS.get(position, {}).get("weight", (160, 300))[1]

    player = {
        "first_name": fake.first_name_male(),
        "last_name": fake.last_name(),
        "height": fake.random_int(min=min_height, max=max_height),
        "weight": fake.random_int(min=min_weight, max=max_weight),
        "age": age,
        "years_pro": years_pro,
        "position": position,
        "overall": overall,
        "jersey_number": 0,  # to be set later
        "stats": stats,
    }

    return player


def write_to_output_file(team_name: str, data: list[dict]):
    team_name = team_name.replace(" ", "_").lower()
    output_dir = dir / "data" / "custom_teams"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{team_name}.json"
    with open(output_file, "w") as f:
        import json

        json.dump(data, f, indent=4)


if __name__ == "__main__":
    for team in TEAMS:
        players = []
        # Simple roster composition
        position_counts = {
            "QB": 2,
            "HB": 4,
            "FB": 1,
            "TE": 3,
            "WR": 5,
            "C": 2,
            "OG": 4,
            "OT": 4,
            "DT": 4,
            "DE": 4,
            "LB": 6,
            "CB": 4,
            "FS": 2,
            "SS": 2,
            "K": 1,
            "P": 1,
        }

        used_numbers = set()
        for position, count in position_counts.items():
            # Gather all possible jersey numbers for this position
            ranges = POSITIONS[position].get("jersey_number_ranges", [(0, 99)])
            possible_numbers = set()
            for r in ranges:
                possible_numbers.update(range(r[0], r[1] + 1))
            # Remove already used numbers
            available_numbers = list(possible_numbers - used_numbers)
            for _ in range(count):
                if not available_numbers:
                    # If we run out, fallback to any unused number
                    jersey_number = next(
                        num for num in range(0, 100) if num not in used_numbers
                    )
                else:
                    jersey_number = fake.random_element(available_numbers)
                    available_numbers.remove(jersey_number)
                used_numbers.add(jersey_number)
                player_data = generate_player_data(position)
                player_data["jersey_number"] = jersey_number
                players.append(player_data)

        # order players by overall within their position, but keeping the position order
        position_order = list(position_counts.keys())
        players.sort(key=lambda p: (position_order.index(p["position"]), -p["overall"]))

        team["players"] = players
        write_to_output_file(team.get("name"), team)
