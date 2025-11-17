from pathlib import Path

from faker import Faker

from colors import get_color

dir = Path(__file__).parent

fake = Faker()


stat_groups = {
    "general": ["awareness", "jumping", "injury", "stamina", "toughness"],
    "speed": ["speed", "acceleration"],
    "power": ["strength", "break_tackle", "trucking", "stiff_arm"],
    "agility": ["agility", "change_of_direction", "spin_move", "juke_move"],
    "ball_carrier": ["carrying", "bc_vision", "break_sack"],
    "route_running": [
        "short_route_running",
        "medium_route_running",
        "deep_route_running",
        "release",
    ],
    "catching": ["catching", "spectacular_catch", "catch_in_traffic"],
    "blocking": [
        "run_block",
        "pass_block",
        "impact_blocking",
        "run_block_power",
        "run_block_finesse",
        "pass_block_power",
        "pass_block_finesse",
        "lead_block",
    ],
    "passing": [
        "throw_power",
        "throw_under_pressure",
        "throw_accuracy_short",
        "throw_accuracy_mid",
        "throw_accuracy_deep",
        "throw_on_the_run",
        "play_action",
    ],
    "defense_general": ["pursuit", "play_recognition"],
    "tackling": ["tackle", "hit_power"],
    "defense_skill": ["power_moves", "finesse_moves", "block_shedding"],
    "zone_coverage": ["zone_coverage"],
    "man_coverage": ["man_coverage", "press"],
    "kicking": ["kick_power", "kick_accuracy"],
    "kick_return": ["kick_return"],
}

ELITE_POTENTIAL = (85, 99)
GREAT_POTENTIAL = (85, 95)
GOOD_POTENTIAL = (75, 85)
AVERAGE_POTENTIAL = (65, 75)
POOR_POTENTIAL = (45, 65)
ABYSMAL_POTENTIAL = (20, 45)

POSITIONS = {
    "QB": {
        "height": (72, 78),
        "weight": (190, 240),
        "stat_ranges": {
            "general": (75, 99),
            "speed": (65, 95),
            "power": (65, 80),
            "agility": (65, 90),
            "ball_carrier": (45, 85),
            "route_running": (20, 65),
            "catching": (20, 65),
            "blocking": ABYSMAL_POTENTIAL,
            "passing": (75, 99),
            "defense_general": ABYSMAL_POTENTIAL,
            "tackling": ABYSMAL_POTENTIAL,
            "defense_skill": ABYSMAL_POTENTIAL,
            "zone_coverage": ABYSMAL_POTENTIAL,
            "man_coverage": ABYSMAL_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(1, 19)],
        "overall_ignore_stat_groups": [
            "blocking",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "HB": {
        "height": (68, 74),
        "weight": (190, 230),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (80, 99),
            "power": (60, 90),
            "agility": (80, 99),
            "ball_carrier": (75, 99),
            "route_running": (55, 85),
            "catching": (55, 85),
            "blocking": (40, 70),
            "passing": POOR_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": (65, 99),
        },
        "jersey_number_ranges": [(0, 39)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "FB": {
        "height": (70, 76),
        "weight": (230, 270),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (60, 80),
            "power": (75, 99),
            "agility": (60, 80),
            "ball_carrier": (60, 85),
            "route_running": (40, 70),
            "catching": (40, 70),
            "blocking": (75, 99),
            "passing": POOR_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": POOR_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 49)],
        "overall_ignore_stat_groups": [
            "passing",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "TE": {
        "height": (74, 80),
        "weight": (240, 280),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (65, 85),
            "power": (70, 95),
            "agility": (65, 85),
            "ball_carrier": (60, 85),
            "route_running": (60, 85),
            "catching": (70, 99),
            "blocking": (65, 95),
            "passing": POOR_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": POOR_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 49), (80, 89)],
        "overall_ignore_stat_groups": [
            "passing",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "WR": {
        "height": (68, 74),
        "weight": (180, 220),
        "stat_ranges": {
            "general": (65, 95),
            "speed": ELITE_POTENTIAL,
            "power": (55, 80),
            "agility": (80, 99),
            "ball_carrier": (65, 90),
            "route_running": (75, 99),
            "catching": (75, 99),
            "blocking": (30, 60),
            "passing": POOR_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": (65, 99),
        },
        "jersey_number_ranges": [(0, 19), (80, 89)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
        ],
    },
    "C": {
        "height": (72, 78),
        "weight": (280, 320),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (50, 70),
            "power": (80, 99),
            "agility": (55, 75),
            "ball_carrier": (30, 60),
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(50, 79)],
        "overall_ignore_stat_groups": [
            "passing",
            "ball_carrier",
            "route_running",
            "catching",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "OG": {
        "height": (72, 78),
        "weight": (280, 320),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (50, 70),
            "power": (80, 99),
            "agility": (55, 75),
            "ball_carrier": (30, 60),
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(50, 79)],
        "overall_ignore_stat_groups": [
            "passing",
            "ball_carrier",
            "route_running",
            "catching",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "OT": {
        "height": (72, 78),
        "weight": (280, 320),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (50, 70),
            "power": (80, 99),
            "agility": (55, 75),
            "ball_carrier": (30, 60),
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (80, 99),
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(50, 79)],
        "overall_ignore_stat_groups": [
            "passing",
            "ball_carrier",
            "route_running",
            "catching",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "DT": {
        "height": (72, 78),
        "weight": (280, 320),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (55, 75),
            "power": (80, 99),
            "agility": (55, 75),
            "ball_carrier": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (70, 95),
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": (65, 95),
            "tackling": (75, 99),
            "defense_skill": (75, 99),
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(50, 79), (90, 99)],
        "overall_ignore_stat_groups": [
            "passing",
            "ball_carrier",
            "route_running",
            "catching",
            "blocking",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "DE": {
        "height": (72, 78),
        "weight": (240, 280),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (65, 85),
            "power": (75, 99),
            "agility": (65, 85),
            "ball_carrier": (30, 60),
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (60, 85),
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": (65, 95),
            "tackling": (70, 95),
            "defense_skill": (70, 95),
            "zone_coverage": (40, 70),
            "man_coverage": (40, 70),
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": POOR_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 59), (90, 99)],
        "overall_ignore_stat_groups": [
            "passing",
            "ball_carrier",
            "route_running",
            "catching",
            "blocking",
            "zone_coverage",
            "man_coverage",
            "kicking",
            "kick_return",
        ],
    },
    "LB": {
        "height": (72, 78),
        "weight": (240, 280),
        "stat_ranges": {
            "general": (70, 99),
            "speed": (65, 85),
            "power": (75, 99),
            "agility": (65, 85),
            "ball_carrier": (30, 60),
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": (60, 85),
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": (70, 99),
            "tackling": (75, 99),
            "defense_skill": (70, 95),
            "zone_coverage": (50, 85),
            "man_coverage": (50, 85),
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": POOR_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 59), (90, 99)],
        "overall_ignore_stat_groups": [
            "passing",
            "ball_carrier",
            "route_running",
            "catching",
            "blocking",
            "kicking",
            "kick_return",
        ],
    },
    "CB": {
        "height": (68, 74),
        "weight": (180, 210),
        "stat_ranges": {
            "general": (65, 95),
            "speed": ELITE_POTENTIAL,
            "power": (50, 75),
            "agility": (80, 99),
            "ball_carrier": (55, 80),
            "route_running": (40, 70),
            "catching": (55, 85),
            "blocking": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": (65, 95),
            "tackling": (55, 85),
            "defense_skill": (65, 95),
            "zone_coverage": (70, 99),
            "man_coverage": (70, 99),
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": (60, 95),
        },
        "jersey_number_ranges": [(0, 49)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "ball_carrier",
            "route_running",
            "kicking",
        ],
    },
    "FS": {
        "height": (70, 76),
        "weight": (190, 220),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (75, 95),
            "power": (55, 80),
            "agility": (75, 95),
            "ball_carrier": (55, 80),
            "route_running": (40, 70),
            "catching": (55, 85),
            "blocking": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": (65, 95),
            "tackling": (60, 90),
            "defense_skill": (60, 90),
            "zone_coverage": (70, 99),
            "man_coverage": (60, 90),
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": (60, 90),
        },
        "jersey_number_ranges": [(0, 49)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "ball_carrier",
            "route_running",
            "kicking",
        ],
    },
    "SS": {
        "height": (70, 76),
        "weight": (190, 220),
        "stat_ranges": {
            "general": (65, 95),
            "speed": (70, 90),
            "power": (60, 90),
            "agility": (70, 90),
            "ball_carrier": (55, 80),
            "route_running": (40, 70),
            "catching": (55, 85),
            "blocking": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": (65, 95),
            "tackling": (65, 95),
            "defense_skill": (65, 95),
            "zone_coverage": (60, 90),
            "man_coverage": (60, 90),
            "kicking": ABYSMAL_POTENTIAL,
            "kick_return": (60, 90),
        },
        "jersey_number_ranges": [(0, 49)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "ball_carrier",
            "route_running",
            "kicking",
        ],
    },
    "K": {
        "height": (68, 74),
        "weight": (180, 220),
        "stat_ranges": {
            "general": (60, 90),
            "speed": (40, 65),
            "power": (40, 65),
            "agility": (40, 65),
            "ball_carrier": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": (75, 99),
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 19)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "ball_carrier",
            "route_running",
            "catching",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kick_return",
        ],
    },
    "P": {
        "height": (68, 74),
        "weight": (180, 220),
        "stat_ranges": {
            "general": (60, 90),
            "speed": (40, 65),
            "power": (40, 65),
            "agility": (40, 65),
            "ball_carrier": ABYSMAL_POTENTIAL,
            "route_running": ABYSMAL_POTENTIAL,
            "catching": ABYSMAL_POTENTIAL,
            "blocking": ABYSMAL_POTENTIAL,
            "passing": ABYSMAL_POTENTIAL,
            "defense_general": POOR_POTENTIAL,
            "tackling": POOR_POTENTIAL,
            "defense_skill": POOR_POTENTIAL,
            "zone_coverage": POOR_POTENTIAL,
            "man_coverage": POOR_POTENTIAL,
            "kicking": (75, 99),
            "kick_return": ABYSMAL_POTENTIAL,
        },
        "jersey_number_ranges": [(0, 19)],
        "overall_ignore_stat_groups": [
            "passing",
            "blocking",
            "ball_carrier",
            "route_running",
            "catching",
            "defense_general",
            "tackling",
            "defense_skill",
            "zone_coverage",
            "man_coverage",
            "kick_return",
        ],
    },
}


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
    overall = total // len(relevant_stats)
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
