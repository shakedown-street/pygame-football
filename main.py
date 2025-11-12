import math
import random
import sys
from typing import Optional

import pygame

from colors import get_color
from rosters import get_by_position

WIDTH = 1280
HEIGHT = WIDTH * (4 / 9)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Football")
clock = pygame.time.Clock()

FRAME_RATE = 60

# FIELD

FIELD_YARDS = 120
FIELD_ASPECT_RATIO = 4 / 9
FIELD_WIDTH = WIDTH
FIELD_HEIGHT = FIELD_WIDTH * FIELD_ASPECT_RATIO
FIELD_CENTER = pygame.Vector2(FIELD_WIDTH / 2, FIELD_HEIGHT / 2)
YARD_LENGTH = WIDTH / FIELD_YARDS
FIELD_HASH_LENGTH = YARD_LENGTH * (2 / 3)
FIELD_HASH_DISTANCE = YARD_LENGTH * 6.16  # NFL standard 6.16
GOAL_POST_WIDTH = YARD_LENGTH * 6.16

# ENTITY SIZES

PLAYER_RADIUS = 6
BALL_RADIUS = 3
HALO_RADIUS = PLAYER_RADIUS * 1.5

# COLLISION PARAMETERS

COLLISION_DISTANCE = PLAYER_RADIUS * 2.2
COLLISION_NUDGE = 0.2
REPULSE_STRENGTH = 0.7

# MOVEMENT PARAMETERS

ACCELERATION_RATE = 0.6
DECELERATION_RATE = 0.7

# Approximate max player speed as 4.2 seconds to run 40 yards
FORTY_YARDS = 40 * YARD_LENGTH
FASTEST_40_TIME = 4.2
n = int(FASTEST_40_TIME * FRAME_RATE)
if ACCELERATION_RATE == 0:
    PLAYER_MAX_SPEED = FORTY_YARDS / FRAME_RATE / 4.2
else:
    denom = n - (1 - (1 - ACCELERATION_RATE) ** n) / ACCELERATION_RATE
    PLAYER_MAX_SPEED = FORTY_YARDS / denom

# THROWING PARAMETERS

THROW_MAX_YARDS = 80
# Higher value = less accurate
THROW_SHORT_DEVIATION_FACTOR = 0.1
THROW_MID_DEVIATION_FACTOR = 0.2
THROW_DEEP_DEVIATION_FACTOR = 0.4
# Higher value = faster throw
THROW_SPEED = 8
# Minimum frames for a short throw
THROW_MIN_FRAMES = 12
# Minimum arc height (in yards)
THROW_MIN_ARC = 30
# Higher value = lower arc
THROW_ARC_DIVISOR = 6

# CATCHING PARAMETERS

# Max height in pixels a catch can be made
CATCH_MAX_HEIGHT = YARD_LENGTH * 2.25
# How close (in pixels) the ball must be to the player to be catchable
CATCH_RADIUS = PLAYER_RADIUS * 2
# If True, catching stat has no effect
PERFECT_CATCHING = False

# BLOCKING PARAMETERS

BLOCK_POINT_FACTOR = 0.3
BLOCK_DISTANCE = PLAYER_RADIUS * 2.5
BLOCK_LATERAL_THRESHOLD = 1

# DEFENSIVE AI PARAMETERS

# Determines how far ahead to lead when pursuing a target
PURSUE_LEAD_FACTOR = 0.6

# Distance to maintain when in man coverage
MAN_COVERAGE_SHADOW_DISTANCE = PLAYER_RADIUS * 3


def get_yard_x(yard):
    start_x = 10 * YARD_LENGTH
    return yard * YARD_LENGTH + start_x


class Game:
    def __init__(self):
        self.down = 1
        self.to_go = 10
        self.ball_position = 20
        self.ball_carrier: Optional[Player] = None


class Field:
    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen, get_color("green", 700), (0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        )

        # Draw endzones

        endzone_1 = pygame.Rect(0, 0, YARD_LENGTH * 10, FIELD_HEIGHT)
        pygame.draw.rect(screen, get_color("blue", 600), endzone_1)
        endzone_2 = pygame.Rect(
            FIELD_WIDTH - YARD_LENGTH * 10, 0, YARD_LENGTH * 10, FIELD_HEIGHT
        )
        pygame.draw.rect(screen, get_color("orange"), endzone_2)

        # Draw hash marks

        for yard in range(11, FIELD_YARDS - 10):  # exclude endzones
            x = yard * YARD_LENGTH

            left_sideline_hash_y = FIELD_HASH_LENGTH
            right_sideline_hash_y = FIELD_HEIGHT - (FIELD_HASH_LENGTH * 2)
            left_middle_hash_y = (
                FIELD_CENTER.y - (FIELD_HASH_DISTANCE / 2) - (FIELD_HASH_LENGTH / 2)
            )
            right_middle_hash_y = (
                FIELD_CENTER.y + (FIELD_HASH_DISTANCE / 2) - (FIELD_HASH_LENGTH / 2)
            )

            for hash_y in [
                left_sideline_hash_y,
                right_sideline_hash_y,
                left_middle_hash_y,
                right_middle_hash_y,
            ]:
                pygame.draw.line(
                    screen,
                    get_color("white"),
                    (x, hash_y),
                    (x, hash_y + FIELD_HASH_LENGTH),
                    2,
                )

        for goal_hash_x in [
            YARD_LENGTH * 12,
            FIELD_WIDTH - YARD_LENGTH * 12,
        ]:
            pygame.draw.line(
                screen,
                get_color("white"),
                (goal_hash_x, FIELD_CENTER.y - (FIELD_HASH_LENGTH)),
                (goal_hash_x, FIELD_CENTER.y + (FIELD_HASH_LENGTH)),
                2,
            )

        # Draw yard lines

        for yard in range(10, FIELD_YARDS - 5, 5):
            x = yard * YARD_LENGTH
            pygame.draw.line(screen, get_color("white"), (x, 0), (x, FIELD_HEIGHT), 2)

        # Draw yard numbers

        for yard in range(10, FIELD_YARDS - 20, 10):
            start_x = 10 * YARD_LENGTH
            x = yard * YARD_LENGTH + start_x

            font = pygame.font.SysFont(None, int(FIELD_HEIGHT // 12))
            number = (
                yard if yard <= (FIELD_YARDS - 20) / 2 else (FIELD_YARDS - 20) - yard
            )
            text = font.render(str(number), True, get_color("white"))
            rotated_text = pygame.transform.rotate(text, 180)
            screen.blit(
                rotated_text,
                (
                    x - rotated_text.get_width() / 2,
                    FIELD_HEIGHT / 6 - (rotated_text.get_height() / 2),
                ),
            )
            screen.blit(
                text,
                (
                    x - text.get_width() / 2,
                    5 * FIELD_HEIGHT / 6 - (text.get_height() / 2),
                ),
            )

        # Draw line of scrimmage

        los_x = get_yard_x(game.ball_position)
        pygame.draw.line(
            screen, get_color("blue", 600), (los_x, 0), (los_x, FIELD_HEIGHT), 2
        )

        # Draw first down line
        fd_x = get_yard_x(game.ball_position + game.to_go)
        pygame.draw.line(
            screen, get_color("yellow", 400), (fd_x, 0), (fd_x, FIELD_HEIGHT), 2
        )

        # Draw goal posts

        goal_post_y = FIELD_CENTER.y - (GOAL_POST_WIDTH / 2)
        pygame.draw.line(
            screen,
            get_color("yellow", 300),
            (0, goal_post_y),
            (12, goal_post_y),
            4,
        )
        pygame.draw.line(
            screen,
            get_color("yellow", 300),
            (0, goal_post_y + GOAL_POST_WIDTH),
            (12, goal_post_y + GOAL_POST_WIDTH),
            4,
        )
        pygame.draw.line(
            screen,
            get_color("yellow", 300),
            (FIELD_WIDTH - 12, goal_post_y),
            (FIELD_WIDTH, goal_post_y),
            4,
        )
        pygame.draw.line(
            screen,
            get_color("yellow", 300),
            (FIELD_WIDTH - 12, goal_post_y + GOAL_POST_WIDTH),
            (FIELD_WIDTH, goal_post_y + GOAL_POST_WIDTH),
            4,
        )


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        color,
        jersey_number=None,
        stats={},
    ):
        super().__init__()
        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.jersey_number = jersey_number
        self.stats = stats
        self.max_speed = PLAYER_MAX_SPEED * (self.stats.get("speed", 50) / 100)
        self.pos = pygame.Vector2(0, 0)
        self.image = pygame.Surface(
            (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            self.image,
            get_color("black"),
            (PLAYER_RADIUS, PLAYER_RADIUS),
            PLAYER_RADIUS,
        )
        pygame.draw.circle(
            self.image, color, (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS - 1
        )
        if self.jersey_number is not None:
            font = pygame.font.SysFont(None, PLAYER_RADIUS * 2)
            text = font.render(str(self.jersey_number), True, get_color("white"))
            text_rect = text.get_rect(center=(PLAYER_RADIUS, PLAYER_RADIUS))
            self.image.blit(text, text_rect)

        self.rect = self.image.get_rect(center=self.pos)

        # Offensive behavior
        self.block_target: Optional[Player] = None
        self.route: list[pygame.Vector2] = []
        self.route_index = 0
        self.running_route = False
        self.reaction_timer = 0
        self.reaction_target: Optional[pygame.Vector2] = None

        # Defensive behavior
        self.pursue_target: Optional[Player] = None
        self.man_coverage_target: Optional[Player] = None

    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = self.pos

    def reset(self):
        self.stop(True)
        self.reset_route()
        self.reset_reaction()
        self.block_target = None
        self.pursue_target = None
        self.man_coverage_target = None

    def reset_to(self, pos: pygame.Vector2):
        self.reset()
        self.set_pos(pos)

    def move(self):
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            # Accelerate toward the desired direction
            desired_velocity = self.direction * self.max_speed
            self.velocity += (desired_velocity - self.velocity) * (
                (self.stats.get("acceleration", 50) / 100) * ACCELERATION_RATE
            )
        else:
            self.velocity *= DECELERATION_RATE

        # Clamp speed to max_speed
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        # Stop very small velocities (to prevent sliding forever)
        if self.velocity.length() < 0.1:
            self.velocity = pygame.Vector2(0, 0)

        self.set_pos(self.pos + self.velocity)

    def stop(self, instant=False):
        self.direction = pygame.Vector2(0, 0)
        if instant:
            self.velocity = pygame.Vector2(0, 0)

    def start_streak_route(self, yards=15, angle=0):
        dx = yards * YARD_LENGTH * math.cos(math.radians(angle))
        dy = yards * YARD_LENGTH * math.sin(math.radians(angle))
        self.route = [pygame.Vector2(self.pos.x + dx, self.pos.y + dy)]
        self.route_index = 0
        self.running_route = True

    # Can be used for any route with one cut: slant, post, out, in
    def start_cut_route(self, yards=15, angle=0, cut_yards=15, cut_angle=15):
        dx1 = yards * YARD_LENGTH * math.cos(math.radians(angle))
        dy1 = yards * YARD_LENGTH * math.sin(math.radians(angle))
        initial = pygame.Vector2(self.pos.x + dx1, self.pos.y + dy1)

        radians = math.radians(cut_angle)
        dx2 = cut_yards * YARD_LENGTH * math.cos(radians)
        dy2 = cut_yards * YARD_LENGTH * math.sin(radians)
        cut_point = pygame.Vector2(initial.x + dx2, initial.y + dy2)

        self.route = [initial, cut_point]
        self.route_index = 0
        self.running_route = True

    def reset_route(self):
        self.route = []
        self.route_index = 0
        self.running_route = False

    def reset_reaction(self):
        self.reaction_timer = 0
        self.reaction_target = None

    def update_block(self, ball_carrier):
        if self.block_target:
            # Calculate the midpoint between defender and ball carrier
            defender = self.block_target
            to_carrier = ball_carrier.pos - defender.pos
            block_point = defender.pos + to_carrier * BLOCK_POINT_FACTOR
            direction = block_point - self.pos
            distance = direction.length()
            if distance > BLOCK_DISTANCE:
                self.direction = direction
            else:
                # Mirror defender's lateral movement (y-axis)
                lateral = pygame.Vector2(0, defender.pos.y - self.pos.y)
                if lateral.length() > BLOCK_LATERAL_THRESHOLD:
                    self.direction = lateral.normalize()
                else:
                    self.stop()

    def update_route(self):
        if self.running_route and len(self.route) > 0:
            direction = self.route[self.route_index] - self.pos
            distance = direction.length()
            if distance < self.max_speed:
                # Reached the route point, go to next or stop
                if self.route_index + 1 < len(self.route):
                    self.route_index += 1
                else:
                    self.reset_route()
                    self.stop()
            else:
                direction = direction.normalize()
                self.direction = direction

    def update_reaction(self):
        if self.reaction_timer > 0:
            self.reaction_timer -= 1
            if self.reaction_timer == 0 and self.reaction_target is not None:
                self.reset_route()
                self.start_streak_route(
                    yards=(self.reaction_target - self.pos).length() / YARD_LENGTH,
                    angle=math.degrees(
                        math.atan2(
                            self.reaction_target.y - self.pos.y,
                            self.reaction_target.x - self.pos.x,
                        )
                    ),
                )
                self.running_route = True
                self.reaction_target = None

    def update_man_coverage(self):
        if self.man_coverage_target:
            target = self.man_coverage_target
            offset = target.pos - self.pos
            distance = offset.length()
            shadow_distance = MAN_COVERAGE_SHADOW_DISTANCE

            if distance > shadow_distance:
                direction = offset.normalize()
                # Add a small random angle
                angle = random.uniform(-0.1, 0.1)
                direction = direction.rotate(math.degrees(angle))
                self.direction = direction
            else:
                self.stop()

    def update_pursue_target(self):
        if self.pursue_target:
            target = self.pursue_target
            distance = (target.pos - self.pos).length()
            if self.max_speed > 0:
                time_to_reach = distance / self.max_speed
            else:
                time_to_reach = 0
            predicted_pos = (
                target.pos + target.velocity * time_to_reach * PURSUE_LEAD_FACTOR
            )
            direction = predicted_pos - self.pos
            if direction.length() > 1:
                self.direction = direction
            else:
                self.stop()

    def update(self):
        self.update_block(game.ball_carrier if game.ball_carrier else qb)
        self.update_route()
        self.update_reaction()
        self.update_man_coverage()
        self.update_pursue_target()
        self.move()

    @classmethod
    def from_roster(cls, team_code, position, index=0):
        color_map = {
            "denver_broncos": get_color("blue"),
            "cincinnati_bengals": get_color("orange"),
            "baltimore_ravens": get_color("purple"),
            "dallas_cowboys": get_color("pink"),
            # Add more team colors as needed
        }
        color = color_map.get(team_code, get_color("black"))
        data = get_by_position(team_code, position)[index]

        stats = data.get("stats", {})
        player_data = {
            "stats": stats,
            "jersey_number": data.get("jersey_number", None),
        }

        return cls(color, **player_data)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(0, 0)
        self.z = 0
        self.velocity = pygame.Vector2(0, 0)
        self.z_velocity = 0
        self.z_gravity = 0
        self.landing_at = pygame.Vector2(0, 0)
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            get_color("yellow", 800),
            (
                BALL_RADIUS,
                BALL_RADIUS,
            ),
            BALL_RADIUS,
        )
        self.rect = self.image.get_rect(center=self.pos)

    def throw_to(self, target_pos: pygame.Vector2, player: Player):
        displacement = target_pos - self.pos
        distance = displacement.length()

        # Cap max distance based on THROW_MAX_YARDS and player's throw power
        max_distance = (
            THROW_MAX_YARDS * (player.stats.get("throw_power", 50) / 100)
        ) * YARD_LENGTH
        if distance > max_distance:
            direction = displacement.normalize()
            target_pos = self.pos + direction * max_distance
            displacement = target_pos - self.pos
            distance = max_distance

        # Calculate throw accuracy and deviation
        if distance <= 20 * YARD_LENGTH:
            accuracy = player.stats.get("throw_accuracy_short", 50)
            deviation_factor = THROW_SHORT_DEVIATION_FACTOR
        elif distance <= 40 * YARD_LENGTH:
            accuracy = player.stats.get("throw_accuracy_mid", 50)
            deviation_factor = THROW_MID_DEVIATION_FACTOR
        else:
            accuracy = player.stats.get("throw_accuracy_deep", 50)
            deviation_factor = THROW_DEEP_DEVIATION_FACTOR

        max_deviation = (100 - accuracy) * deviation_factor
        angle_deviation = random.uniform(-max_deviation, max_deviation)

        print(
            f"throw_distance_yards={distance / YARD_LENGTH:.1f}, accuracy={accuracy}, angle_deviation={angle_deviation:.1f}"
        )

        # Adjust target position based on deviation
        if distance > 0:
            direction = (target_pos - self.pos).normalize()
            direction = direction.rotate(angle_deviation)
            target_pos = self.pos + direction * distance
            displacement = target_pos - self.pos
            distance = displacement.length()

        self.landing_at = target_pos.copy()

        # Calculate number of frames for the throw
        n_frames = max(THROW_MIN_FRAMES, int(distance / THROW_SPEED))
        self.velocity = displacement / n_frames

        # Calculate arc parameters
        arc_height = max(THROW_MIN_ARC, distance / THROW_ARC_DIVISOR)
        half_frames = n_frames / 2
        self.z = 0
        self.z_velocity = 2 * arc_height / half_frames
        self.z_gravity = (2 * arc_height) / (half_frames**2)
        self.frames_left = n_frames

        # print(
        #     f"n_frames={n_frames}, velocity={self.velocity}, arc_height={arc_height}, z={self.z}, z_velocity={self.z_velocity}, z_gravity={self.z_gravity}"
        # )

    def stop(self):
        self.z = 0
        self.velocity = pygame.Vector2(0, 0)
        self.z_velocity = 0
        self.z_gravity = 0
        self.landing_at = pygame.Vector2(0, 0)
        self.frames_left = 0

    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = self.pos

    def reset_to(self, pos: pygame.Vector2):
        self.stop()
        self.set_pos(pos)

    def update(self):
        if getattr(self, "frames_left", 0) > 0:
            self.set_pos(self.pos + self.velocity)
            self.z += self.z_velocity
            self.z_velocity -= self.z_gravity
            self.frames_left -= 1
            if self.z < 0:
                self.stop()
            # print(
            #     f"frames_left={self.frames_left}, pos={self.pos}, z={self.z}, z_yards={self.z / YARD_LENGTH} z_velocity={self.z_velocity}"
            # )
        else:
            # Ball has landed, stop movement
            self.stop()


class Halo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(0, 0)
        self.image = pygame.Surface((HALO_RADIUS * 2, HALO_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            self.image,
            get_color("yellow", 300),
            (HALO_RADIUS, HALO_RADIUS),
            HALO_RADIUS,
            1,
        )
        self.rect = self.image.get_rect(center=self.pos)

    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = self.pos


def move_ball_carrier(keys):
    if game.ball_carrier is None:
        return

    dx, dy = 0, 0
    if keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_s]:
        dy += 1
    if keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_d]:
        dx += 1

    if dx != 0 or dy != 0:
        game.ball_carrier.direction = pygame.Vector2(dx, dy).normalize()
    else:
        game.ball_carrier.stop()


def avoid_player_collisions(players, min_distance):
    player_list = list(players)
    for i in range(len(player_list)):
        for j in range(i + 1, len(player_list)):
            p1 = player_list[i]
            p2 = player_list[j]
            offset = p1.pos - p2.pos
            dist = offset.length()
            if dist < min_distance and dist > 0:
                # Calculate repulsion direction
                repulse = offset.normalize()
                # Add a small random "bobble" nudge
                angle = random.uniform(-1 * COLLISION_NUDGE, COLLISION_NUDGE)
                repulse = repulse.rotate(math.degrees(angle))
                move_amount = (min_distance - dist) / 2

                p1_factor = p1.velocity.length() * p1.stats.get("strength", 50)
                p2_factor = p2.velocity.length() * p2.stats.get("strength", 50)
                total_factor = p1_factor + p2_factor

                if total_factor > 0:
                    p1_share = p2_factor / total_factor
                    p2_share = p1_factor / total_factor
                else:
                    # If both are still, use only strength
                    total_strength = p1.stats.get("strength", 50) + p2.stats.get(
                        "strength", 50
                    )
                    if total_strength > 0:
                        p1_share = p2.stats.get("strength", 50) / total_strength
                        p2_share = p1.stats.get("strength", 50) / total_strength
                    else:
                        p1_share = p2_share = 0.5

                repulse_vector = repulse * move_amount * REPULSE_STRENGTH
                p1.velocity += repulse_vector * p1_share
                p2.velocity -= repulse_vector * p2_share


game = Game()
field = Field()

# Offensive formation (shotgun)
lt_pos = pygame.Vector2(get_yard_x(game.ball_position - 0.5), FIELD_CENTER.y - 30)
lg_pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y - 15)
c_pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y)
rg_pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y + 15)
rt_pos = pygame.Vector2(get_yard_x(game.ball_position - 0.5), FIELD_CENTER.y + 30)
qb_pos = pygame.Vector2(get_yard_x(game.ball_position - 5), FIELD_CENTER.y)
hb_pos = pygame.Vector2(get_yard_x(game.ball_position - 5), FIELD_CENTER.y - 20)
te_pos = pygame.Vector2(get_yard_x(game.ball_position - 1), FIELD_CENTER.y + 45)
wr_1_pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y - 120)
wr_2_pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y + 120)
wr_3_pos = pygame.Vector2(get_yard_x(game.ball_position - 1), FIELD_CENTER.y - 80)

# Defensive formation (nickel 2-4)
ledg_pos = pygame.Vector2(get_yard_x(game.ball_position + 1), FIELD_CENTER.y - 45)
ldt_pos = pygame.Vector2(get_yard_x(game.ball_position + 1), FIELD_CENTER.y - 15)
rdt_pos = pygame.Vector2(get_yard_x(game.ball_position + 1), FIELD_CENTER.y + 15)
redg_pos = pygame.Vector2(get_yard_x(game.ball_position + 1), FIELD_CENTER.y + 45)
cb_1_pos = pygame.Vector2(get_yard_x(game.ball_position + 10), FIELD_CENTER.y - 180)
cb_2_pos = pygame.Vector2(get_yard_x(game.ball_position + 10), FIELD_CENTER.y + 180)
cb_3_pos = pygame.Vector2(get_yard_x(game.ball_position + 2), FIELD_CENTER.y - 80)
mike_pos = pygame.Vector2(get_yard_x(game.ball_position + 4), FIELD_CENTER.y - 15)
will_pos = pygame.Vector2(get_yard_x(game.ball_position + 4), FIELD_CENTER.y + 15)
fs_pos = pygame.Vector2(get_yard_x(game.ball_position + 11), FIELD_CENTER.y - 60)
ss_pos = pygame.Vector2(get_yard_x(game.ball_position + 11), FIELD_CENTER.y + 60)

# Create offensive players
lt = Player.from_roster("denver_broncos", "LT")
lg = Player.from_roster("denver_broncos", "LG")
c = Player.from_roster("denver_broncos", "C")
rg = Player.from_roster("denver_broncos", "RG")
rt = Player.from_roster("denver_broncos", "RT")
qb = Player.from_roster("denver_broncos", "QB")
hb = Player.from_roster("denver_broncos", "HB")
te = Player.from_roster("denver_broncos", "TE")
wr_1 = Player.from_roster("denver_broncos", "WR", index=0)
wr_2 = Player.from_roster("denver_broncos", "WR", index=1)
wr_3 = Player.from_roster("denver_broncos", "WR", index=2)

# Create defensive players
ledg = Player.from_roster("dallas_cowboys", "LEDG")
ldt = Player.from_roster("dallas_cowboys", "DT", index=0)
rdt = Player.from_roster("dallas_cowboys", "DT", index=1)
redg = Player.from_roster("dallas_cowboys", "REDG")
cb_1 = Player.from_roster("dallas_cowboys", "CB", index=0)
cb_2 = Player.from_roster("dallas_cowboys", "CB", index=1)
cb_3 = Player.from_roster("dallas_cowboys", "CB", index=2)
mike = Player.from_roster("dallas_cowboys", "MIKE")
will = Player.from_roster("dallas_cowboys", "WILL")
fs = Player.from_roster("dallas_cowboys", "FS")
ss = Player.from_roster("dallas_cowboys", "SS")

# Create ball and halo
ball = Ball()
halo = Halo()

game.ball_carrier = c

oline = pygame.sprite.Group(lt, lg, c, rg, rt)
dline = pygame.sprite.Group(ledg, ldt, rdt, redg)
receivers = pygame.sprite.Group(wr_1, wr_2, wr_3, te, hb)
offense = pygame.sprite.Group(oline, qb, receivers)
defense = pygame.sprite.Group(dline, cb_1, cb_2, cb_3, mike, will, fs, ss)
all_players = pygame.sprite.Group(offense, defense)


def reset_play():
    # Reset offense
    lt.reset_to(lt_pos.copy())
    lg.reset_to(lg_pos.copy())
    c.reset_to(c_pos.copy())
    rg.reset_to(rg_pos.copy())
    rt.reset_to(rt_pos.copy())
    qb.reset_to(qb_pos.copy())
    hb.reset_to(hb_pos.copy())
    te.reset_to(te_pos.copy())
    wr_1.reset_to(wr_1_pos.copy())
    wr_2.reset_to(wr_2_pos.copy())
    wr_3.reset_to(wr_3_pos.copy())
    # Reset defense
    ledg.reset_to(ledg_pos.copy())
    ldt.reset_to(ldt_pos.copy())
    rdt.reset_to(rdt_pos.copy())
    redg.reset_to(redg_pos.copy())
    cb_1.reset_to(cb_1_pos.copy())
    cb_2.reset_to(cb_2_pos.copy())
    cb_3.reset_to(cb_3_pos.copy())
    mike.reset_to(mike_pos.copy())
    will.reset_to(will_pos.copy())
    fs.reset_to(fs_pos.copy())
    ss.reset_to(ss_pos.copy())
    # reset ball position
    ball.reset_to(c_pos.copy())
    game.ball_carrier = c


reset_play()


while True:
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.ball_carrier == c:
                    # Snap ball to qb and start play
                    game.ball_carrier = qb
                    wr_1.start_cut_route(yards=10, angle=0, cut_yards=35, cut_angle=90)
                    cb_1.man_coverage_target = wr_1
                    wr_2.start_cut_route(yards=3, angle=15, cut_yards=35, cut_angle=0)
                    cb_2.man_coverage_target = wr_2
                    wr_3.start_cut_route(yards=12, angle=0, cut_yards=35, cut_angle=45)
                    cb_3.man_coverage_target = wr_3
                    hb.start_cut_route(yards=8, angle=-40, cut_yards=18, cut_angle=-75)
                    mike.man_coverage_target = hb
                    te.start_streak_route(yards=20, angle=75)
                    will.man_coverage_target = te
                    # make all oline puruse nearest defender
                    for blocker in oline:
                        nearest_defender = min(
                            dline,
                            key=lambda defender: (defender.pos - blocker.pos).length(),
                        )
                        blocker.block_target = nearest_defender
                    # make all dline pursue qb
                    # for defender in dline:
                    #     defender.pursue_target = qb
                elif game.ball_carrier == qb:
                    # Throw ball to mouse position
                    qb.stop()
                    game.ball_carrier = None
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    ball.throw_to(mouse_pos.copy(), qb)
                    landing_at = ball.landing_at
                    # Make nearest receiver run towards the ball
                    nearest_receiver = min(
                        receivers,
                        key=lambda receiver: (receiver.pos - landing_at).length(),
                    )
                    min_frames = int(FRAME_RATE * 0.25)
                    max_frames = int(FRAME_RATE * 0.5)
                    reaction_frames = int(
                        max_frames
                        - (nearest_receiver.stats.get("awareness", 50) / 100)
                        * (max_frames - min_frames)
                    )
                    nearest_receiver.reaction_timer = reaction_frames
                    nearest_receiver.reaction_target = ball.landing_at.copy()
                    print("Reaction frames:", reaction_frames)
            if event.key == pygame.K_r:
                reset_play()

    move_ball_carrier(keys)
    all_players.update()
    avoid_player_collisions(all_players, COLLISION_DISTANCE)

    if game.ball_carrier:
        ball.set_pos(game.ball_carrier.pos.copy())
    else:
        ball.update()
        if ball.z == 0:
            for receiver in receivers:
                receiver.reset_reaction()
        if ball.z > 0 and ball.z < CATCH_MAX_HEIGHT:
            for receiver in receivers:
                catch_rect = pygame.Rect(
                    receiver.pos.x - CATCH_RADIUS,
                    receiver.pos.y - CATCH_RADIUS,
                    CATCH_RADIUS * 2,
                    CATCH_RADIUS * 2,
                )

                if ball.rect.colliderect(catch_rect):
                    ball.stop()
                    receiver.reset_reaction()
                    # Even a perfectly rated receiver can drop a pass occasionally
                    random_roll = random.randint(1, 101)
                    print(
                        f"roll={random_roll} catching={receiver.stats.get('catching', 50)}"
                    )
                    if (
                        random_roll <= receiver.stats.get("catching", 50)
                        or PERFECT_CATCHING
                    ):
                        game.ball_carrier = receiver
                        receiver.reset_route()
                        for defender in defense:
                            defender.pursue_target = receiver
                    else:
                        print("Dropped pass!")

    # if game.ball_carrier:
    #     for defender in defense:
    #         if defender.rect.colliderect(game.ball_carrier.rect):
    #             yards_gained = (
    #                 game.ball_carrier.pos.x / YARD_LENGTH - 10
    #             ) - game.ball_position
    #             print(f"Tackle! {yards_gained:.1f} yards gained.")
    #             reset_play()

    # endzone_rect = pygame.Rect(
    #     FIELD_WIDTH - YARD_LENGTH * 10, 0, YARD_LENGTH * 10, FIELD_HEIGHT
    # )
    # if game.ball_carrier and endzone_rect.colliderect(game.ball_carrier.rect):
    #     print("Touchdown!")
    #     reset_play()

    # Make halo follow ball
    halo.set_pos(ball.pos.copy())

    field.draw(screen)
    all_players.draw(screen)

    for player in receivers:
        catch_rect = pygame.Rect(
            player.pos.x - CATCH_RADIUS,
            player.pos.y - CATCH_RADIUS,
            CATCH_RADIUS * 2,
            CATCH_RADIUS * 2,
        )

        pygame.draw.rect(screen, get_color("white", 100), catch_rect, 1)

    # Draw receiver routes
    for receiver in receivers:
        if receiver.running_route:
            for i in range(receiver.route_index, len(receiver.route)):
                start_pos = (
                    receiver.pos if i == receiver.route_index else receiver.route[i - 1]
                )
                end_pos = receiver.route[i]
                pygame.draw.line(
                    screen,
                    get_color("yellow", 400),
                    start_pos,
                    end_pos,
                    1,
                )

    screen.blit(ball.image, ball.rect)
    screen.blit(halo.image, halo.rect)

    pygame.display.flip()
    clock.tick(FRAME_RATE)
