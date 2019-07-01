from legionarek.constants import NUMBER_OF_LIVES


class Player():
    def __init__(self, name, color, pos_x, pos_y):
        self.name = name
        self.lives = NUMBER_OF_LIVES
        self.dead = False
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.dead = True
        return self.dead

    def _move_up_down(self, where):
        self.pos_y += where

    def _move_left_right(self, where):
        self.pos_x += where

    def move_up(self):
        self._move_up_down(-1)

    def move_down(self):
        self._move_up_down(1)

    def move_left(self):
        self._move_left_right(-1)

    def move_right(self):
        self._move_left_right(1)

    @property
    def position(self):
        return (self.pos_x, self.pos_y)
