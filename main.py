import math
import random
import sys
from typing import Optional

import pygame

from colors import get_color

WIDTH = 1280
HEIGHT = WIDTH * (4 / 9)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Football")
clock = pygame.time.Clock()

FRAME_RATE = 60

FIELD_YARDS = 120
FIELD_ASPECT_RATIO = 4 / 9
FIELD_WIDTH = WIDTH
FIELD_HEIGHT = FIELD_WIDTH * FIELD_ASPECT_RATIO
FIELD_CENTER = pygame.Vector2(FIELD_WIDTH / 2, FIELD_HEIGHT / 2)
YARD_LENGTH = WIDTH / FIELD_YARDS
FIELD_HASH_LENGTH = YARD_LENGTH * (2 / 3)
FIELD_HASH_DISTANCE = YARD_LENGTH * 6.16  # NFL standard 6.16
GOAL_POST_WIDTH = YARD_LENGTH * 6.16


# Approximate max speed as 4.2 seconds to run 40 yards
FORTY_YARDS = 40 * YARD_LENGTH
PLAYER_MAX_SPEED = FORTY_YARDS / FRAME_RATE / 4.2

PLAYER_RADIUS = 6
BALL_RADIUS = 3
HALO_RADIUS = PLAYER_RADIUS * 1.25


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
    def __init__(self, x, y, color, speed=50):
        super().__init__()
        self.speed = speed
        self.pos = pygame.Vector2(x, y)
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
        self.rect = self.image.get_rect(center=self.pos)

        # Offensive behavior
        self.block_target: Optional[Player] = None
        self.running_route = False
        self.route_target = None

        # Defensive behavior
        self.pursue_target: Optional[Player] = None
        self.man_coverage_target: Optional[Player] = None

    def move_speed_per_frame(self):
        return PLAYER_MAX_SPEED * (self.speed / 100)

    def move(self, direction: pygame.Vector2):
        self.pos.x += direction.x * self.move_speed_per_frame()
        self.pos.y += direction.y * self.move_speed_per_frame()
        self.rect.center = self.pos

    def start_streak_route(self, yards=15):
        dx = yards * YARD_LENGTH
        dy = 0
        self.route_target = pygame.Vector2(self.pos.x + dx, self.pos.y + dy)
        self.running_route = True

    def update_block(self, ball_carrier):
        if self.block_target:
            # Calculate the midpoint between defender and ball carrier
            defender = self.block_target
            to_carrier = ball_carrier.pos - defender.pos
            block_point = defender.pos + to_carrier * 0.3  # 0.3 = stand between
            direction = block_point - self.pos
            distance = direction.length()
            if distance > PLAYER_RADIUS * 2.5:
                self.move(direction.normalize())
            else:
                # Mirror defender's lateral movement (y-axis)
                lateral = pygame.Vector2(0, defender.pos.y - self.pos.y)
                if lateral.length() > 1:
                    self.move(lateral.normalize())

    def update_route(self):
        if self.running_route and self.route_target:
            direction = self.route_target - self.pos
            distance = direction.length()
            if distance < self.move_speed_per_frame():
                self.pos = self.route_target
                self.running_route = False
            else:
                direction = direction.normalize()
                self.move(direction)

    def update_man_coverage(self):
        if self.man_coverage_target:
            offset = self.man_coverage_target.pos - self.pos
            distance = offset.length()
            shadow_distance = PLAYER_RADIUS * 1.5
            if distance > shadow_distance:
                direction = offset.normalize()
                # Add a small random angle
                angle = random.uniform(-0.1, 0.1)
                direction = direction.rotate(math.degrees(angle))
                self.move(direction)

    def update_pursue_target(self):
        if self.pursue_target:
            direction = self.pursue_target.pos - self.pos
            if direction.length() > 1:
                self.move(direction.normalize())


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
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

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos
        self.velocity *= 0.98  # Simulate friction


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


game = Game()
field = Field()

PLAYER_COLOR = get_color("blue", 600)

lt = Player(get_yard_x(game.ball_position), FIELD_CENTER.y - 30, PLAYER_COLOR, 75)
lg = Player(get_yard_x(game.ball_position), FIELD_CENTER.y - 15, PLAYER_COLOR, 75)
c = Player(get_yard_x(game.ball_position), FIELD_CENTER.y, PLAYER_COLOR, 75)
rg = Player(get_yard_x(game.ball_position), FIELD_CENTER.y + 15, PLAYER_COLOR, 75)
rt = Player(get_yard_x(game.ball_position), FIELD_CENTER.y + 30, PLAYER_COLOR, 75)
qb = Player(get_yard_x(game.ball_position - 5), FIELD_CENTER.y, PLAYER_COLOR, 80)
wr_1 = Player(get_yard_x(game.ball_position), FIELD_CENTER.y + 120, PLAYER_COLOR, 95)
wr_2 = Player(get_yard_x(game.ball_position), FIELD_CENTER.y - 120, PLAYER_COLOR, 95)

lde = Player(
    get_yard_x(game.ball_position + 1), FIELD_CENTER.y - 30, get_color("orange"), 75
)
ldt = Player(
    get_yard_x(game.ball_position + 1), FIELD_CENTER.y - 15, get_color("orange"), 75
)
rdt = Player(
    get_yard_x(game.ball_position + 1), FIELD_CENTER.y + 15, get_color("orange"), 75
)
rde = Player(
    get_yard_x(game.ball_position + 1), FIELD_CENTER.y + 30, get_color("orange"), 75
)
cb_1 = Player(
    get_yard_x(game.ball_position + 10), FIELD_CENTER.y + 120, get_color("orange"), 92
)
cb_2 = Player(
    get_yard_x(game.ball_position + 15), FIELD_CENTER.y - 120, get_color("orange"), 92
)

ball = Ball()
halo = Halo()

game.ball_carrier = c

oline = pygame.sprite.Group(lt, lg, c, rg, rt)
dline = pygame.sprite.Group(lde, ldt, rdt, rde)
offense = pygame.sprite.Group(oline, qb, wr_1, wr_2)
defense = pygame.sprite.Group(dline, cb_1, cb_2)
all_players = pygame.sprite.Group(offense, defense)

BALL_THROW_SPEED = 16


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
        direction = pygame.Vector2(dx, dy).normalize()
        game.ball_carrier.move(direction)


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
                angle = random.uniform(-0.5, 0.5)
                repulse = repulse.rotate(math.degrees(angle))
                move_amount = (min_distance - dist) / 2
                p1.pos += repulse * move_amount
                p2.pos -= repulse * move_amount
                p1.rect.center = p1.pos
                p2.rect.center = p2.pos


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
                    wr_1.start_streak_route(yards=50)
                    cb_1.man_coverage_target = wr_1
                    wr_2.start_streak_route(yards=50)
                    cb_2.man_coverage_target = wr_2
                    # make all oline puruse nearest defender
                    for blocker in oline:
                        nearest_defender = min(
                            dline,
                            key=lambda defender: (defender.pos - blocker.pos).length(),
                        )
                        blocker.block_target = nearest_defender
                    # make all dline pursue qb
                    for defender in dline:
                        defender.pursue_target = qb
                elif game.ball_carrier == qb:
                    # Throw ball to mouse position
                    game.ball_carrier = None
                    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
                    direction = mouse_pos - ball.pos
                    if direction.length() != 0:
                        direction = direction.normalize()
                    else:
                        direction = pygame.Vector2(0, 0)
                    ball.velocity = direction * BALL_THROW_SPEED
            if event.key == pygame.K_r:
                # Reset

                # Reset offense positions
                lt.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y - 30
                )
                lt.rect.center = lt.pos
                lg.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y - 15
                )
                lg.rect.center = lg.pos
                c.pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y)
                c.rect.center = c.pos
                rg.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y + 15
                )
                rg.rect.center = rg.pos
                rt.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y + 30
                )
                rt.rect.center = rt.pos
                qb.pos = pygame.Vector2(
                    get_yard_x(game.ball_position - 5), FIELD_CENTER.y
                )
                qb.rect.center = qb.pos
                wr_1.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y + 120
                )
                wr_1.rect.center = wr_1.pos
                wr_2.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y - 120
                )
                wr_2.rect.center = wr_2.pos
                # Reset defense positions
                cb_1.pos = pygame.Vector2(
                    get_yard_x(game.ball_position + 10), FIELD_CENTER.y + 120
                )
                cb_1.rect.center = cb_1.pos
                cb_2.pos = pygame.Vector2(
                    get_yard_x(game.ball_position + 15), FIELD_CENTER.y - 120
                )
                cb_2.rect.center = cb_2.pos
                lde.pos = pygame.Vector2(
                    get_yard_x(game.ball_position + 2), FIELD_CENTER.y - 30
                )
                lde.rect.center = lde.pos
                ldt.pos = pygame.Vector2(
                    get_yard_x(game.ball_position + 2), FIELD_CENTER.y - 15
                )
                ldt.rect.center = ldt.pos
                rdt.pos = pygame.Vector2(
                    get_yard_x(game.ball_position + 2), FIELD_CENTER.y + 15
                )
                rdt.rect.center = rdt.pos
                rde.pos = pygame.Vector2(
                    get_yard_x(game.ball_position + 2), FIELD_CENTER.y + 30
                )
                rde.rect.center = rde.pos
                # reset state
                # reset oline
                for blocker in oline:
                    blocker.block_target = None
                # reset dline
                for defender in dline:
                    defender.pursue_target = None
                wr_1.running_route = False
                wr_1.route_target = None
                wr_2.running_route = False
                wr_2.route_target = None
                cb_1.man_coverage_target = None
                cb_2.man_coverage_target = None
                # reset ball position
                ball.pos = c.pos.copy()
                ball.rect.center = c.pos.copy()
                ball.velocity = pygame.Vector2(0, 0)
                halo.pos = c.pos.copy()
                halo.rect.center = c.pos.copy()
                game.ball_carrier = c

    wr_1.update_route()
    wr_2.update_route()
    cb_1.update_man_coverage()
    cb_2.update_man_coverage()
    cb_1.update_pursue_target()
    cb_2.update_pursue_target()
    for blocker in oline:
        blocker.update_block(game.ball_carrier if game.ball_carrier else qb)
    for defender in dline:
        defender.update_pursue_target()
    move_ball_carrier(keys)
    avoid_player_collisions(all_players, PLAYER_RADIUS * 2.5)

    if game.ball_carrier:
        ball.pos = game.ball_carrier.pos.copy()
        ball.rect.center = game.ball_carrier.pos.copy()
    else:
        ball.update()
        for wr in [wr_1, wr_2]:
            if halo.rect.colliderect(wr.rect):
                game.ball_carrier = wr
                wr.running_route = False
                wr.route_target = None
                for defender in dline:
                    defender.pursue_target = wr
                ball.velocity = pygame.Vector2(0, 0)

    # Make halo follow ball
    halo.pos = ball.pos.copy()
    halo.rect.center = ball.pos.copy()

    field.draw(screen)
    all_players.draw(screen)

    screen.blit(ball.image, ball.rect)
    screen.blit(halo.image, halo.rect)

    pygame.display.flip()
    clock.tick(FRAME_RATE)
