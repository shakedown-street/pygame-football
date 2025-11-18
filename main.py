import math
import random
import sys
from typing import Optional

import pygame

from colors import get_color
from config import (
    ACCELERATION_RATE,
    BALL_RADIUS,
    CATCH_MAX_HEIGHT,
    CATCH_RADIUS,
    COLLISION_DISTANCE,
    COLLISION_NUDGE,
    COLLISION_REPULSION_FACTOR,
    DECELERATION_RATE,
    FIELD_CENTER,
    FIELD_HEIGHT,
    FRAME_RATE,
    HALO_RADIUS,
    HEIGHT,
    PERFECT_CATCHING,
    PERFECT_THROWING,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    THROW_ARC_DIVISOR,
    THROW_DEVIATION_FACTOR,
    THROW_MAX_YARDS,
    THROW_MIN_ARC,
    THROW_MIN_FRAMES,
    THROW_SPEED,
    WIDTH,
    YARD_LENGTH,
)
from field import Field
from team import Team, load_teams
from utils import get_yard_x

TEAMS = load_teams()


def get_team(name: str):
    return [team for team in TEAMS if team.name == name][0]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Football")
clock = pygame.time.Clock()

ball_on_yard = 20
yards_to_go = 10
ball_carrier: Optional["Player"] = None
play_selected = 0


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        team: Team,
        info={},
        stats={},
    ):
        super().__init__()
        self.pos = pygame.Vector2(0, 0)
        self.direction = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.info = info
        self.stats = stats
        self.max_speed = PLAYER_MAX_SPEED * (self.stats.get("speed", 50) / 100)

        # Offensive behavior
        self.route: list[pygame.Vector2] = []
        self.route_index = 0
        self.running_route = False
        self.reaction_timer = 0
        self.reaction_target: Optional[pygame.Vector2] = None

        self.image = pygame.Surface(
            (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(center=self.pos)

        # Draw player circle
        pygame.draw.circle(
            self.image,
            team.secondary_color,
            (PLAYER_RADIUS, PLAYER_RADIUS),
            PLAYER_RADIUS,
        )
        pygame.draw.circle(
            self.image,
            team.primary_color,
            (PLAYER_RADIUS, PLAYER_RADIUS),
            PLAYER_RADIUS - 1,
        )
        # Draw jersey number
        font = pygame.font.SysFont(None, PLAYER_RADIUS * 2)
        text = font.render(
            str(self.info.get("jersey_number", 0)), True, team.secondary_color
        )
        text_rect = text.get_rect(center=(PLAYER_RADIUS, PLAYER_RADIUS))
        self.image.blit(text, text_rect)

    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = self.pos

    def move(self):
        if self.direction.length() > 0:
            desired_velocity = self.direction * self.max_speed
            offset = desired_velocity - self.velocity
            self.velocity += offset * (
                (self.stats.get("acceleration", 50) / 100) * ACCELERATION_RATE
            )
        else:
            # Gradually decelerate if no direction is given
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

    def set_route(self, routes: list[dict]):
        routes_points = []

        for i, route in enumerate(routes):
            yards = route.get("yards", 0)
            angle = route.get("angle", 0)

            if i == 0:
                dx = yards * YARD_LENGTH * math.cos(math.radians(angle))
                dy = yards * YARD_LENGTH * math.sin(math.radians(angle))
                point = pygame.Vector2(self.pos.x + dx, self.pos.y + dy)
                routes_points.append(point)
            else:
                prev_point = routes_points[i - 1]
                radians = math.radians(angle)
                dx = yards * YARD_LENGTH * math.cos(radians)
                dy = yards * YARD_LENGTH * math.sin(radians)
                point = pygame.Vector2(prev_point.x + dx, prev_point.y + dy)
                routes_points.append(point)

        self.route = routes_points
        self.route_index = 0

    def start_route(self):
        self.route_index = 0
        self.running_route = True

    def reset_route(self):
        self.route = []
        self.route_index = 0
        self.running_route = False

    def reset_reaction(self):
        self.reaction_timer = 0
        self.reaction_target = None

    def reset(self):
        self.stop(True)
        self.reset_route()
        self.reset_reaction()

    def reset_to(self, pos: pygame.Vector2):
        self.reset()
        self.set_pos(pos)

    def estimate_position(self, frames: int) -> pygame.Vector2:
        """Estimate where the player will be after n frames"""
        pos = self.pos.copy()
        speed = self.max_speed
        remaining_frames = frames

        if self.running_route:
            route = self.route[self.route_index :]

            for i, point in enumerate(route):
                direction = point.copy() - pos
                distance = direction.length()
                if distance == 0:
                    continue
                direction = direction.normalize()
                frames_to_point = (
                    int(distance / speed) if speed > 0 else remaining_frames
                )
                if frames_to_point >= remaining_frames:
                    # Will not reach this point within the remaining frames
                    pos += direction * speed * remaining_frames
                    return pos
                else:
                    # Move to this point and continue to next
                    pos = point.copy()
                    remaining_frames -= frames_to_point

            # If route ends before frames run out, keep moving in last direction
            if route:
                direction = (
                    (route[-1] - pos).normalize()
                    if (route[-1] - pos).length() > 0
                    else pygame.Vector2(0, 0)
                )
                pos += direction * speed * remaining_frames

            return pos

        # Not running a route, just keep moving in current direction
        if self.velocity.length() < 0.1:
            return pos
        pos += self.velocity.copy() * remaining_frames
        return pos

    def update_route(self):
        # Handle reacting to a throw
        if self.reaction_timer > 0:
            self.reaction_timer -= 1
            if self.reaction_timer == 0 and self.reaction_target is not None:
                self.reset_route()

                yards = (self.reaction_target - self.pos).length() / YARD_LENGTH
                angle = math.degrees(
                    math.atan2(
                        self.reaction_target.y - self.pos.y,
                        self.reaction_target.x - self.pos.x,
                    )
                )

                self.set_route([{"yards": yards, "angle": angle}])
                self.start_route()
                self.reaction_target = None

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

    def update(self):
        self.update_route()
        self.move()

    def __str__(self):
        name = f"{self.info.get('first_name', '')} {self.info.get('last_name', '')}"
        number = self.info.get("jersey_number", 0)
        overall = self.info.get("overall", 50)
        speed = self.stats.get("speed", 50)
        strength = self.stats.get("strength", 50)
        agility = self.stats.get("agility", 50)
        awareness = self.stats.get("awareness", 50)
        max_speed = self.max_speed
        return f"{name} (#{number}) [overall={overall} speed={speed} strength={strength} agility={agility} awareness={awareness}]"

    @classmethod
    def from_roster(cls, team: Team, position: str, index=0):
        data = team.get_players_by_position(position)[index]

        info = {
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "height": data.get("height", 70),
            "weight": data.get("weight", 200),
            "age": data.get("age", 25),
            "years_pro": data.get("years_pro", 0),
            "position": data.get("position", ""),
            "overall": data.get("overall", 50),
            "jersey_number": data.get("jersey_number", 0),
        }
        stats = data.get("stats", {})
        player_data = {
            "team": team,
            "info": info,
            "stats": stats,
        }

        return cls(**player_data)


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
        self.rect = self.image.get_rect(center=self.pos)

        # Draw ball circle
        pygame.draw.circle(
            self.image,
            get_color("yellow", 800),
            (
                BALL_RADIUS,
                BALL_RADIUS,
            ),
            BALL_RADIUS,
        )

    def throw_to(self, target_pos: pygame.Vector2, player: Player, lob=False):
        throw_power = player.stats.get("throw_power", 50)
        throw_accuracy = player.stats.get("throw_accuracy", 50)

        offset = target_pos - self.pos
        distance = offset.length()

        throw_speed = max(2, THROW_SPEED * (throw_power / 100))
        throw_min_frames = THROW_MIN_FRAMES
        throw_min_arc = THROW_MIN_ARC
        throw_arc_divisor = THROW_ARC_DIVISOR

        # Adjust parameters for lob throws
        if lob:
            throw_speed *= 0.7
            throw_min_frames *= 1.5
            throw_min_arc *= 1.5
            throw_arc_divisor /= 1.5
            throw_accuracy *= 0.9

        # Adjust target position based on throw power
        max_distance = THROW_MAX_YARDS * YARD_LENGTH * (throw_power / 100)
        if distance > max_distance:
            direction = offset.normalize()
            target_pos = self.pos + direction * max_distance
            offset = target_pos - self.pos
            distance = max_distance

        # Calculate random angle deviation based on throw_accuracy
        max_deviation = (100 - throw_accuracy) * THROW_DEVIATION_FACTOR
        angle_deviation = (
            random.uniform(-max_deviation, max_deviation) if not PERFECT_THROWING else 0
        )

        # Adjust target position based on deviation
        if distance > 0:
            direction = (target_pos - self.pos).normalize()
            direction = direction.rotate(angle_deviation)
            target_pos = self.pos + direction * distance
            offset = target_pos - self.pos
            distance = offset.length()

        self.landing_at = target_pos.copy()

        # Calculate number of frames for the throw
        n_frames = max(throw_min_frames, int(distance / throw_speed))
        self.velocity = offset / n_frames

        # Calculate arc parameters
        arc_height = max(throw_min_arc, distance / throw_arc_divisor)
        half_frames = n_frames / 2
        self.z = 0
        self.z_velocity = 2 * arc_height / half_frames
        self.z_gravity = (2 * arc_height) / (half_frames**2)
        self.frames_left = n_frames

        print(
            f"Ball thrown [throw_power={throw_power} throw_accuracy={throw_accuracy:.1f} distance_yards={distance / YARD_LENGTH:.1f} throw_speed={throw_speed:.1f} angle_deviation={angle_deviation:.1f} max_height={arc_height / YARD_LENGTH:.1f} n_frames={n_frames}]"
        )

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
            self.z += self.z_velocity
            self.z_velocity -= self.z_gravity
            self.frames_left -= 1
            if self.z < 0:
                self.stop()
            self.set_pos(self.pos + self.velocity)
        else:
            self.stop()


class Halo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(0, 0)
        self.image = pygame.Surface((HALO_RADIUS * 2, HALO_RADIUS * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        # Draw halo circle
        pygame.draw.circle(
            self.image,
            get_color("yellow", 300),
            (HALO_RADIUS, HALO_RADIUS),
            HALO_RADIUS,
            1,
        )

    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = self.pos


def move_ball_carrier(keys: pygame.key.ScancodeWrapper):
    if ball_carrier is None:
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
        ball_carrier.direction = pygame.Vector2(dx, dy).normalize()
    else:
        ball_carrier.stop()


def handle_player_collisions(players: list[Player], min_distance: float):
    player_list = list(players)
    for i in range(len(player_list)):
        for j in range(i + 1, len(player_list)):
            p1 = player_list[i]
            p2 = player_list[j]
            offset = p1.pos - p2.pos
            distance = offset.length()
            if distance < min_distance and distance > 0:
                repulse = offset.normalize()

                # Add a small random "bobble" nudge
                angle = random.uniform(-1 * COLLISION_NUDGE, COLLISION_NUDGE)
                repulse = repulse.rotate(math.degrees(angle))

                move_amount = (min_distance - distance) / 2

                p1_weight = p1.info.get("weight", 200)
                p1_strength = p1.stats.get("strength", 50)
                p1_agility = p1.stats.get("agility", 50)
                p1_momentum = p1_weight * p1_strength * p1.velocity.length()

                p2_weight = p2.info.get("weight", 200)
                p2_strength = p2.stats.get("strength", 50)
                p2_agility = p2.stats.get("agility", 50)
                p2_momentum = p2_weight * p2_strength * p2.velocity.length()

                # prevent division by zero
                total_momentum = p1_momentum + p2_momentum + 1e-5

                p1_push = (p2_momentum / total_momentum) * (1 - p1_agility / 400)
                p2_push = (p1_momentum / total_momentum) * (1 - p2_agility / 400)

                repulse_vector = repulse * move_amount * COLLISION_REPULSION_FACTOR
                p1.velocity += repulse_vector * p1_push
                p2.velocity -= repulse_vector * p2_push


field = Field()

# Offensive formation (shotgun)
lt_pos = pygame.Vector2(get_yard_x(ball_on_yard - 0.5), FIELD_CENTER.y - 30)
lg_pos = pygame.Vector2(get_yard_x(ball_on_yard), FIELD_CENTER.y - 15)
c_pos = pygame.Vector2(get_yard_x(ball_on_yard), FIELD_CENTER.y)
rg_pos = pygame.Vector2(get_yard_x(ball_on_yard), FIELD_CENTER.y + 15)
rt_pos = pygame.Vector2(get_yard_x(ball_on_yard - 0.5), FIELD_CENTER.y + 30)
qb_pos = pygame.Vector2(get_yard_x(ball_on_yard - 5), FIELD_CENTER.y)
hb_pos = pygame.Vector2(get_yard_x(ball_on_yard - 5), FIELD_CENTER.y + 20)
te_pos = pygame.Vector2(get_yard_x(ball_on_yard - 1), FIELD_CENTER.y + 45)
wr_1_pos = pygame.Vector2(get_yard_x(ball_on_yard - 1), FIELD_CENTER.y - 160)
wr_2_pos = pygame.Vector2(get_yard_x(ball_on_yard - 2), FIELD_CENTER.y - 120)
wr_3_pos = pygame.Vector2(get_yard_x(ball_on_yard - 2), FIELD_CENTER.y - 80)

# Defensive formation (nickel 2-4)
# ledg_pos = pygame.Vector2(get_yard_x(ball_on_yard + 1), FIELD_CENTER.y - 45)
# ldt_pos = pygame.Vector2(get_yard_x(ball_on_yard + 1), FIELD_CENTER.y - 15)
# rdt_pos = pygame.Vector2(get_yard_x(ball_on_yard + 1), FIELD_CENTER.y + 15)
# redg_pos = pygame.Vector2(get_yard_x(ball_on_yard + 1), FIELD_CENTER.y + 45)
# cb_1_pos = pygame.Vector2(get_yard_x(ball_on_yard + 10), FIELD_CENTER.y - 180)
# cb_2_pos = pygame.Vector2(get_yard_x(ball_on_yard + 2), FIELD_CENTER.y - 80)
# cb_3_pos = pygame.Vector2(get_yard_x(ball_on_yard + 10), FIELD_CENTER.y + 180)
# mike_pos = pygame.Vector2(get_yard_x(ball_on_yard + 4), FIELD_CENTER.y - 15)
# will_pos = pygame.Vector2(get_yard_x(ball_on_yard + 4), FIELD_CENTER.y + 15)
# fs_pos = pygame.Vector2(get_yard_x(ball_on_yard + 11), FIELD_CENTER.y - 60)
# ss_pos = pygame.Vector2(get_yard_x(ball_on_yard + 11), FIELD_CENTER.y + 60)

# Create offensive players
offense_team = get_team("Warforge")

lt = Player.from_roster(offense_team, "OT", index=0)
lg = Player.from_roster(offense_team, "OG", index=0)
c = Player.from_roster(offense_team, "C", index=0)
rg = Player.from_roster(offense_team, "OG", index=1)
rt = Player.from_roster(offense_team, "OT", index=1)
qb = Player.from_roster(offense_team, "QB", index=0)
hb = Player.from_roster(offense_team, "HB", index=0)
te = Player.from_roster(offense_team, "TE", index=0)
wr_1 = Player.from_roster(offense_team, "WR", index=0)
wr_2 = Player.from_roster(offense_team, "WR", index=1)
wr_3 = Player.from_roster(offense_team, "WR", index=2)

# Create ball and halo
ball = Ball()
halo = Halo()

oline = pygame.sprite.Group(lt, lg, c, rg, rt)
receivers = pygame.sprite.Group(wr_1, wr_2, wr_3, te, hb)
offense = pygame.sprite.Group(oline, qb, receivers)
all_players = pygame.sprite.Group(offense)


def reset_play():
    global ball_carrier
    ball_carrier = c
    # reset offense
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
    # reset ball position
    ball.reset_to(c_pos.copy())
    # set play routes
    if play_selected == 0:
        wr_1.set_route([{"yards": 2, "angle": -10}, {"yards": 25, "angle": 0}])
        wr_2.set_route([{"yards": 10, "angle": 10}, {"yards": 25, "angle": 35}])
        wr_3.set_route(
            [
                {"yards": 3, "angle": 0},
                {"yards": 8, "angle": 35},
                {"yards": 25, "angle": 60},
            ]
        )
        hb.set_route([{"yards": 6, "angle": 90}, {"yards": 12, "angle": 60}])
        te.set_route([{"yards": 3, "angle": -10}, {"yards": 20, "angle": -75}])
    if play_selected == 1:
        wr_1.set_route([{"yards": 5, "angle": 0}, {"yards": 20, "angle": 20}])
        wr_2.set_route([{"yards": 3, "angle": 0}, {"yards": 15, "angle": -30}])
        wr_3.set_route([{"yards": 2, "angle": -5}, {"yards": 10, "angle": 0}])
        hb.set_route([{"yards": 4, "angle": 45}, {"yards": 10, "angle": 90}])
        te.set_route([{"yards": 5, "angle": -15}, {"yards": 15, "angle": -45}])
    if play_selected == 2:
        wr_1.set_route([{"yards": 2, "angle": -10}, {"yards": 25, "angle": 0}])
        wr_2.set_route([{"yards": 2, "angle": 10}, {"yards": 25, "angle": 0}])
        wr_3.set_route([{"yards": 2, "angle": 0}, {"yards": 25, "angle": 0}])
        hb.set_route([{"yards": 5, "angle": 90}])
        te.set_route([{"yards": 3, "angle": -5}, {"yards": 25, "angle": -20}])


def handle_snap():
    global ball_carrier
    ball_carrier = qb
    for receiver in receivers:
        receiver.start_route()
    print(f"Ball snapped to {qb}")


def handle_throw(lob=False):
    global ball_carrier
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    ball.throw_to(mouse_pos.copy(), ball_carrier, lob)
    ball_carrier.stop()
    ball_carrier = None
    handle_receiver_reaction()


def handle_receiver_reaction():
    landing_at = ball.landing_at

    # Make nearest receiver run towards the ball
    flight_frames = ball.frames_left
    landing_at = ball.landing_at

    def future_distance(receiver):
        future_pos = receiver.estimate_position(flight_frames)
        return (future_pos - landing_at).length()

    nearest_receiver = min(receivers, key=future_distance)
    awareness = nearest_receiver.stats.get("awareness", 50)
    min_frames = int(FRAME_RATE * 0.25)
    max_frames = int(FRAME_RATE * 0.5)
    reaction_frames = int(max_frames - (awareness / 100) * (max_frames - min_frames))
    nearest_receiver.reaction_timer = reaction_frames
    nearest_receiver.reaction_target = landing_at.copy()
    print(f"Reacted to throw [reaction_frames={reaction_frames}]")


reset_play()


while True:
    #########
    # EVENT #
    #########

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Standard pass to mouse position
                handle_throw(lob=False)

            if event.button == 3:
                # Lob pass to mouse position
                handle_throw(lob=True)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if ball_carrier == c:
                    handle_snap()
            if event.key == pygame.K_r:
                reset_play()
            if event.key == pygame.K_1:
                play_selected = 0
                reset_play()
            if event.key == pygame.K_2:
                play_selected = 1
                reset_play()
            if event.key == pygame.K_3:
                play_selected = 2
                reset_play()

    ##########
    # UPDATE #
    ##########

    move_ball_carrier(keys)
    all_players.update()
    handle_player_collisions(all_players, COLLISION_DISTANCE)

    if ball_carrier:
        ball.set_pos(ball_carrier.pos.copy())
    else:
        ball.update()
        if ball.z == 0:
            for receiver in receivers:
                receiver.reset_reaction()
        else:
            for receiver in receivers:
                catch_rect = pygame.Rect(
                    receiver.pos.x - CATCH_RADIUS,
                    receiver.pos.y - CATCH_RADIUS,
                    CATCH_RADIUS * 2,
                    CATCH_RADIUS * 2,
                )

                if ball.z > 0 and ball.z < CATCH_MAX_HEIGHT:
                    if ball.rect.colliderect(catch_rect):
                        catching = receiver.stats.get("catching", 50)
                        # Even a perfectly rated receiver can drop a pass occasionally
                        random_roll = random.randint(1, 100)
                        print(
                            f"Attempting catch [z_yards={ball.z/YARD_LENGTH:.2f} catching={catching} random_roll={random_roll}]"
                        )
                        ball.stop()
                        receiver.reset_reaction()
                        if random_roll <= catching or PERFECT_CATCHING:
                            print(f"Pass completed to {receiver}!")
                            ball_carrier = receiver
                            receiver.reset_route()
                        else:
                            print(f"Pass dropped by {receiver}!")

    # Make halo follow ball
    halo.set_pos(ball.pos.copy())

    ########
    # DRAW #
    ########

    screen.fill((0, 0, 0))

    screen.blit(field.image, field.rect)

    # Draw line of scrimmage

    los_x = get_yard_x(ball_on_yard)
    pygame.draw.line(
        screen, get_color("blue", 600), (los_x, 0), (los_x, FIELD_HEIGHT), 2
    )

    # Draw first down line
    fd_x = get_yard_x(ball_on_yard + yards_to_go)
    pygame.draw.line(
        screen, get_color("yellow", 400), (fd_x, 0), (fd_x, FIELD_HEIGHT), 2
    )

    all_players.draw(screen)

    # for player in all_players:
    #     # Draw estimated position after 60 frames
    #     future_pos = player.estimate_position(
    #         ball.frames_left if ball.frames_left > 0 else 60
    #     )
    #     pygame.draw.circle(
    #         screen,
    #         get_color("red"),
    #         (future_pos.x, future_pos.y),
    #         2,
    #         2,
    #     )

    # Draw ball and halo

    screen.blit(ball.image, ball.rect)
    screen.blit(halo.image, halo.rect)

    # Draw ball landing position

    if ball_carrier is None and ball.frames_left > 0:
        pygame.draw.circle(
            screen,
            get_color("white"),
            (ball.landing_at.x, ball.landing_at.y),
            PLAYER_RADIUS,
            1,
        )

    for receiver in receivers:
        # Draw catch radius around receivers
        catch_rect = pygame.Rect(
            receiver.pos.x - CATCH_RADIUS,
            receiver.pos.y - CATCH_RADIUS,
            CATCH_RADIUS * 2,
            CATCH_RADIUS * 2,
        )

        pygame.draw.rect(screen, get_color("white"), catch_rect, 1)

        # Draw routes
        if receiver.route:
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

    pygame.display.flip()
    clock.tick(FRAME_RATE)
