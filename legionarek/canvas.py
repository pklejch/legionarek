import legionarek.constants


class Canvas():
    def __init__(self, width, height, cards):
        # type: (int, int, List[Card]) -> ()
        self.width = width
        self.height = height
        self.cards = cards
        self.canvas = [[None for x in range(width)] for y in range(height)]

    def render(self):
        # type: () -> (List[List[Card]])
        for i in range(self.width):
            for j in range(self.height):
                self.canvas[i][j] = self.canvas[i+j]
        return self.canvas
