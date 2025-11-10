import math
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

        self.running_route = False
        self.route_target = None

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

c = Player(get_yard_x(game.ball_position), FIELD_CENTER.y, PLAYER_COLOR, 60)
qb = Player(get_yard_x(game.ball_position - 5), FIELD_CENTER.y, PLAYER_COLOR, 75)
wr = Player(get_yard_x(game.ball_position), FIELD_CENTER.y + 120, PLAYER_COLOR, 96)

ball = Ball()
halo = Halo()

game.ball_carrier = c

all_players = pygame.sprite.Group(c, qb, wr)

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
                    # Snap ball to qb and start route for wr
                    game.ball_carrier = qb
                    wr.start_streak_route(yards=12)
                elif game.ball_carrier == qb:
                    # Throw ball to wr
                    game.ball_carrier = None
                    direction = (wr.pos - ball.pos).normalize()
                    ball.velocity = direction * BALL_THROW_SPEED
                elif game.ball_carrier != qb:
                    # Throw back to c
                    game.ball_carrier = c
            if event.key == pygame.K_r:
                # Reset
                c.pos = pygame.Vector2(get_yard_x(game.ball_position), FIELD_CENTER.y)
                c.rect.center = c.pos
                qb.pos = pygame.Vector2(
                    get_yard_x(game.ball_position - 5), FIELD_CENTER.y
                )
                qb.rect.center = qb.pos
                wr.pos = pygame.Vector2(
                    get_yard_x(game.ball_position), FIELD_CENTER.y + 120
                )
                wr.rect.center = wr.pos
                wr.running_route = False
                wr.route_target = None
                ball.pos = c.pos.copy()
                ball.rect.center = c.pos.copy()
                ball.velocity = pygame.Vector2(0, 0)
                halo.pos = c.pos.copy()
                halo.rect.center = c.pos.copy()
                game.ball_carrier = c

    wr.update_route()
    move_ball_carrier(keys)

    if game.ball_carrier:
        ball.pos = game.ball_carrier.pos.copy()
        ball.rect.center = game.ball_carrier.pos.copy()
        halo.pos = game.ball_carrier.pos.copy()
        halo.rect.center = game.ball_carrier.pos.copy()
    else:
        ball.update()
        halo.pos = ball.pos.copy()
        halo.rect.center = ball.pos.copy()
        if ball.rect.colliderect(wr.rect):
            game.ball_carrier = wr
            ball.velocity = pygame.Vector2(0, 0)

    field.draw(screen)
    all_players.draw(screen)

    screen.blit(ball.image, ball.rect)
    screen.blit(halo.image, halo.rect)

    pygame.display.flip()
    clock.tick(FRAME_RATE)
