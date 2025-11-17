from pathlib import Path

from faker import Faker

dir = Path(__file__).parent

fake = Faker()

GENERAL_STATS = [
    "speed",
    "acceleration",
    "strength",
    "agility",
    "awareness",
    "jumping",
    "injury",
    "stamina",
    "toughness",
]

BALL_CARRIER_STATS = [
    "carrying",
    "break_tackle",
    "trucking",
    "change_of_direction",
    "bc_vision",
    "stiff_arm",
    "spin_move",
    "juke_move",
    "break_sack",
    "kick_return",
]

BLOCKING_STATS = [
    "run_block",
    "pass_block",
    "impact_blocking",
    "run_block_power",
    "run_block_finesse",
    "pass_block_power",
    "pass_block_finesse",
    "lead_block",
]

PASSING_STATS = [
    "throw_power",
    "throw_under_pressure",
    "throw_accuracy_short",
    "throw_accuracy_mid",
    "throw_accuracy_deep",
    "throw_on_the_run",
    "play_action",
]

DEFENSE_STATS = [
    "tackle",
    "power_moves",
    "finesse_moves",
    "block_shedding",
    "pursuit",
    "play_recognition",
    "man_coverage",
    "zone_coverage",
    "hit_power",
    "press",
]

RECEIVING_STATS = [
    "catching",
    "spectacular_catch",
    "catch_in_traffic",
    "short_route_running",
    "medium_route_running",
    "deep_route_running",
    "release",
]

KICKING_STATS = [
    "kick_power",
    "kick_accuracy",
]


POSITIONS = {
    "QB": {
        "height": (72, 78),
        "weight": (190, 240),
        "primary_stats": GENERAL_STATS + PASSING_STATS,
        "secondary_stats": BALL_CARRIER_STATS,
        "jersey_number_ranges": [
            (1, 19),
        ],
    },
    "HB": {
        "height": (68, 74),
        "weight": (190, 230),
        "primary_stats": GENERAL_STATS + BALL_CARRIER_STATS,
        "secondary_stats": RECEIVING_STATS + BLOCKING_STATS,
        "jersey_number_ranges": [
            (0, 39),
        ],
    },
    "FB": {
        "height": (70, 76),
        "weight": (230, 270),
        "primary_stats": GENERAL_STATS + BLOCKING_STATS,
        "secondary_stats": BALL_CARRIER_STATS + RECEIVING_STATS,
        "jersey_number_ranges": [
            (0, 49),
        ],
    },
    "TE": {
        "height": (74, 80),
        "weight": (240, 280),
        "primary_stats": GENERAL_STATS + RECEIVING_STATS + BALL_CARRIER_STATS,
        "secondary_stats": BLOCKING_STATS,
        "jersey_number_ranges": [
            (0, 49),
            (80, 89),
        ],
    },
    "WR": {
        "height": (68, 74),
        "weight": (180, 220),
        "primary_stats": GENERAL_STATS + RECEIVING_STATS + BALL_CARRIER_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 19),
            (80, 89),
        ],
    },
    "C": {
        "height": (72, 78),
        "weight": (280, 320),
        "primary_stats": GENERAL_STATS + BLOCKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (50, 79),
        ],
    },
    "LG": {
        "height": (72, 78),
        "weight": (280, 320),
        "primary_stats": GENERAL_STATS + BLOCKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (50, 79),
        ],
    },
    "LT": {
        "height": (72, 78),
        "weight": (280, 320),
        "primary_stats": GENERAL_STATS + BLOCKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (50, 79),
        ],
    },
    "RG": {
        "height": (72, 78),
        "weight": (280, 320),
        "primary_stats": GENERAL_STATS + BLOCKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (50, 79),
        ],
    },
    "RT": {
        "height": (72, 78),
        "weight": (280, 320),
        "primary_stats": GENERAL_STATS + BLOCKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (50, 79),
        ],
    },
    "DT": {
        "height": (72, 78),
        "weight": (280, 320),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (50, 79),
            (90, 99),
        ],
    },
    "LEDG": {
        "height": (72, 78),
        "weight": (240, 280),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 59),
            (90, 99),
        ],
    },
    "MIKE": {
        "height": (72, 78),
        "weight": (240, 280),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 59),
            (90, 99),
        ],
    },
    "REDG": {
        "height": (72, 78),
        "weight": (240, 280),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 59),
            (90, 99),
        ],
    },
    "SAM": {
        "height": (72, 78),
        "weight": (240, 280),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 59),
            (90, 99),
        ],
    },
    "WILL": {
        "height": (72, 78),
        "weight": (240, 280),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 59),
            (90, 99),
        ],
    },
    "CB": {
        "height": (68, 74),
        "weight": (180, 210),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": RECEIVING_STATS,
        "jersey_number_ranges": [
            (0, 49),
        ],
    },
    "FS": {
        "height": (70, 76),
        "weight": (190, 220),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": RECEIVING_STATS,
        "jersey_number_ranges": [
            (0, 49),
        ],
    },
    "SS": {
        "height": (70, 76),
        "weight": (190, 220),
        "primary_stats": GENERAL_STATS + DEFENSE_STATS,
        "secondary_stats": RECEIVING_STATS,
        "jersey_number_ranges": [
            (0, 49),
        ],
    },
    "K": {
        "height": (68, 74),
        "weight": (180, 220),
        "primary_stats": GENERAL_STATS + KICKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 19),
        ],
    },
    "P": {
        "height": (68, 74),
        "weight": (180, 220),
        "primary_stats": GENERAL_STATS + KICKING_STATS,
        "secondary_stats": [],
        "jersey_number_ranges": [
            (0, 19),
        ],
    },
}


def speed_range(position: str) -> tuple[int, int]:
    position_info = POSITIONS.get(position, {})
    height_range = position_info.get("height", (68, 80))
    weight_range = position_info.get("weight", (160, 300))

    fast_positions = {
        "HB",
        "TE",
        "WR",
        "CB",
        "FS",
        "SS",
    }
    mid_speed_positions = {
        "QB",
        "FB",
        "LEDG",
        "MIKE",
        "REDG",
        "SAM",
        "WILL",
    }

    if position in fast_positions:
        base_speed = 90
    elif position in mid_speed_positions:
        base_speed = 83
    else:
        base_speed = 75

    # Softer penalties
    min_speed = max(
        50, base_speed - (weight_range[1] - 180) // 8 - (height_range[0] - 70) // 2
    )
    max_speed = min(
        99,
        base_speed - (weight_range[0] - 180) // 14 - (height_range[1] - 70) // 3 + 12,
    )

    # Ensure min_speed <= max_speed
    if min_speed > max_speed:
        min_speed, max_speed = max_speed, min_speed

    return (min_speed, max_speed)


for position in POSITIONS.keys():
    POSITIONS[position]["speed_range"] = speed_range(position)
    print(f"{position}: {POSITIONS[position]['speed_range']}")


def generate_stat_ratings(position) -> dict:
    stats = {}

    position_info = POSITIONS.get(position, {})
    primary_stats = set(position_info.get("primary_stats", []))
    secondary_stats = set(position_info.get("secondary_stats", []))

    # Gather all possible stats
    all_stats = (
        set(GENERAL_STATS)
        | set(BALL_CARRIER_STATS)
        | set(BLOCKING_STATS)
        | set(PASSING_STATS)
        | set(DEFENSE_STATS)
        | set(RECEIVING_STATS)
        | set(KICKING_STATS)
    )

    for stat in all_stats:
        if stat in primary_stats:
            stats[stat] = fake.random_int(min=75, max=99)
        elif stat in secondary_stats:
            stats[stat] = fake.random_int(min=60, max=74)
        else:
            stats[stat] = fake.random_int(min=20, max=59)

    # Apply speed range
    min_speed, max_speed = position_info.get("speed_range", (60, 99))
    stats["speed"] = fake.random_int(min=min_speed, max=max_speed)

    # Acceleration correlated with speed
    speed = stats["speed"]
    accel_min = max(50, speed - 10)
    accel_max = min(99, speed + 5)
    stats["acceleration"] = fake.random_int(min=accel_min, max=accel_max)

    return stats


def calculate_overall(position: str, stats: dict) -> int:
    """
    Calculates a player's overall rating based on their position's primary and secondary stats.
    """
    position_info = POSITIONS.get(position, {})
    primary_stats = position_info.get("primary_stats", [])
    secondary_stats = position_info.get("secondary_stats", [])

    primary_values = [stats[s] for s in primary_stats if s in stats]
    secondary_values = [stats[s] for s in secondary_stats if s in stats]

    values_sum = sum(primary_values) + sum(secondary_values)
    values_count = len(primary_values) + len(secondary_values)

    if values_count == 0:
        return 0.0

    overall = values_sum / values_count
    return round(overall)


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
    output_dir = dir / "output"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{team_name}.json"
    with open(output_file, "w") as f:
        import json

        json.dump(data, f, indent=4)


TEAM_NAMES = [
    "Wildcats",
    "Titans",
    "Dragons",
    "Stallions",
    "Vipers",
    "Warriors",
    "Raptors",
    "Bulldogs",
    "Pirates",
    "Knights",
    "Sharks",
    "Falcons",
    "Spartans",
    "Phantoms",
    "Crusaders",
    "Mustangs",
    "Rebels",
    "Cougars",
]


if __name__ == "__main__":
    for team_name in TEAM_NAMES:
        roster = []
        # Simple roster composition
        position_counts = {
            "QB": 2,
            "HB": 4,
            "FB": 1,
            "TE": 3,
            "WR": 5,
            "C": 2,
            "LG": 2,
            "LT": 2,
            "RG": 2,
            "RT": 2,
            "DT": 4,
            "LEDG": 2,
            "MIKE": 2,
            "REDG": 2,
            "SAM": 2,
            "WILL": 2,
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
                roster.append(player_data)

        write_to_output_file(team_name, roster)
