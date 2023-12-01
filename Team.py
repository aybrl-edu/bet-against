class Team:
    def __init__(self, name, win_p):
        self.name = name
        self.win_p = win_p

    def __repr__(self):
        return f"{self.name}:{self.win_p}"