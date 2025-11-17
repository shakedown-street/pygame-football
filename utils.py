from config import YARD_LENGTH


def get_yard_x(yard: float) -> float:
    start_x = 10 * YARD_LENGTH
    return yard * YARD_LENGTH + start_x
