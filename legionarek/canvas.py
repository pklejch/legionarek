from legionarek.constants import CANVAS_WIDTH
from random import shuffle


class Canvas():
    def __init__(self, width, height, cards):
        # type: (int, int, List[Card]) -> ()
        self.width = width
        self.height = height
        self.cards = cards
        shuffle(self.cards)
        self.canvas = [[None for x in range(width)] for y in range(height)]

    def render(self):
        # type: () -> (List[List[Card]])
        for i in range(self.height):
            for j in range(self.width):
                self.canvas[i][j] = self.cards[i * CANVAS_WIDTH + j]
        return self.canvas

    def flip_card(self, pos_x, pos_y):
        return self.canvas[pos_x][pos_y].flip()
