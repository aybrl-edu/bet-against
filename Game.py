# G set of games, where g ∈ G is defined as : g <- ^T1(^P)-^T2(^P):^P where (T1, T2 ∈ T : string (team names)) & P ∈
# Pr is the probability of the event
class Game:
    def __init__(self, t1, t2, draw_p):
        self.t1 = t1
        self.t2 = t2
        self.name = f"{t1.name}-{t2.name}"
        self.draw_p = draw_p

    def __repr__(self):
        return f"{self.name}: {repr(self.t1)} - {repr(self.t2)} - {self.draw_p}"
