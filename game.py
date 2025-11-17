class Game:
    def __init__(self):
        self.home_team = None
        self.away_team = None
        self.quarter = 1
        self.time = 4 * 60
        self.possession = None
        self.down = 1
        self.yard_to_go = 10
        self.ball_on = 35
        self.home_score = 0
        self.away_score = 0
