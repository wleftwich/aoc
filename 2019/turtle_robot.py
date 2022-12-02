class TurtleBot:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.drxn = 'N'
        self.painted = {}

    def paint_turn_move(self, p, t):
        self.painted[(self.x, self.y)] = p
        self.turn(t)
        self.move()

    def turn(self, t):
        compass = {
            'N': ['W', 'E'],
            'E': ['N', 'S'],
            'S': ['E', 'W'],
            'W': ['S', 'N']
        }
        self.drxn = compass[self.drxn][t]

    def move(self):
        if self.drxn == 'N':
            self.y += 1
        elif self.drxn == 'E':
            self.x += 1
        elif self.drxn == 'S':
            self.y -= 1
        elif self.drxn == 'W':
            self.x -= 1

    def get_color(self):
        return self.painted.get((self.x, self.y), 0)







