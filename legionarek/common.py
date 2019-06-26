import random


class Dice():
    @staticmethod
    def roll():
        return random.randint(1, 6)

    @staticmethod
    def double_roll():
        return Dice.roll() + Dice.roll()
