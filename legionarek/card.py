import abc
from legionarek.common import Dice


class CardConfig:
    def __init__(self, front_side, back_side, message):
        self.front_side = front_side
        self.back_side = back_side
        self.visible_side = back_side
        self.message = message


class Card(abc.ABC):
    def __init__(self, config):
        self.config = config

    def flip(self):
        self.config.visible_side = self.config.front_side
        return self._is_successful()

    def display(self):
        print(self.config.message)

    def __str__(self):
        return f'Card: message: {self.config.message}'

    @abc.abstractmethod
    def _is_successful(self):
        pass


class CombatCard(Card):
    def __init__(self, config, power):
        super().__init__(config)
        self.power = power

    def _fight(self):
        while True:
            roll = Dice.double_roll()
            print('You rolled', roll)
            if roll != self.power:
                break
        return roll > self.power

    def _is_successful(self):
        won = self._fight()
        if won:
            print('You have won.')
        else:
            print('You have lost.')

        return won

    def __str__(self):
        return f'Combat Card, message: {self.config.message}, power: {self.power}'


class LetterCard(Card):
    def _is_successful(self):
        return False


class TaskCard(Card):
    def _is_successful(self, task_done):
        return task_done


class QuizCard(Card):
    def _is_successful(self, answer):
        return answer
