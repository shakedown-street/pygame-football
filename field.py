import pygame

from colors import get_color
from config import (
    FIELD_CENTER,
    FIELD_HASH_DISTANCE,
    FIELD_HASH_LENGTH,
    FIELD_HEIGHT,
    FIELD_WIDTH,
    FIELD_YARDS,
    GOAL_POST_WIDTH,
    YARD_LENGTH,
)


class Field:
    def __init__(self):
        self.image = pygame.Surface((FIELD_WIDTH, FIELD_HEIGHT))
        self.rect = self.image.get_rect(topleft=(0, 0))

        self.draw(self.image)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface, get_color("green", 700), (0, 0, FIELD_WIDTH, FIELD_HEIGHT)
        )

        # Draw endzones

        endzone_1 = pygame.Rect(0, 0, YARD_LENGTH * 10, FIELD_HEIGHT)
        pygame.draw.rect(surface, get_color("blue", 600), endzone_1)
        endzone_2 = pygame.Rect(
            FIELD_WIDTH - YARD_LENGTH * 10, 0, YARD_LENGTH * 10, FIELD_HEIGHT
        )
        pygame.draw.rect(surface, get_color("orange"), endzone_2)

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
                    surface,
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
                surface,
                get_color("white"),
                (goal_hash_x, FIELD_CENTER.y - (FIELD_HASH_LENGTH)),
                (goal_hash_x, FIELD_CENTER.y + (FIELD_HASH_LENGTH)),
                2,
            )

        # Draw yard lines

        for yard in range(10, FIELD_YARDS - 5, 5):
            x = yard * YARD_LENGTH
            pygame.draw.line(surface, get_color("white"), (x, 0), (x, FIELD_HEIGHT), 2)

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
            surface.blit(
                rotated_text,
                (
                    x - rotated_text.get_width() / 2,
                    FIELD_HEIGHT / 6 - (rotated_text.get_height() / 2),
                ),
            )
            surface.blit(
                text,
                (
                    x - text.get_width() / 2,
                    5 * FIELD_HEIGHT / 6 - (text.get_height() / 2),
                ),
            )

        # Draw goal posts

        goal_post_y = FIELD_CENTER.y - (GOAL_POST_WIDTH / 2)
        pygame.draw.line(
            surface,
            get_color("yellow", 300),
            (0, goal_post_y),
            (12, goal_post_y),
            4,
        )
        pygame.draw.line(
            surface,
            get_color("yellow", 300),
            (0, goal_post_y + GOAL_POST_WIDTH),
            (12, goal_post_y + GOAL_POST_WIDTH),
            4,
        )
        pygame.draw.line(
            surface,
            get_color("yellow", 300),
            (FIELD_WIDTH - 12, goal_post_y),
            (FIELD_WIDTH, goal_post_y),
            4,
        )
        pygame.draw.line(
            surface,
            get_color("yellow", 300),
            (FIELD_WIDTH - 12, goal_post_y + GOAL_POST_WIDTH),
            (FIELD_WIDTH, goal_post_y + GOAL_POST_WIDTH),
            4,
        )
