import abc
from legionarek.common import Dice


class CardConfig:
    def __init__(self, front_side, back_side, message):
        self.front_side = front_side
        self.back_side = back_side
        self.visible_side = back_side
        self.message = message

    def __str__(self):
        return f'{self.front_side}, {self.back_side}, {self.message}'


class CombatCardConfig(CardConfig):
    def __init__(self, front_side, back_side, message, power):
        super().__init__(front_side, back_side, message)
        self.power = power


class TaskCardConfig(CardConfig):
    def __init__(self, front_side, back_side, message, task):
        super().__init__(front_side, back_side, message)
        self.task = task


class LetterCardConfig(CardConfig):
    def __init__(self, front_side, back_side, message):
        super().__init__(front_side, back_side, message)


class QuizCardConfig(CardConfig):
    def __init__(self, front_side, back_side, message, question_a, question_b, question_c, answer_a, answer_b, answer_c):
        super().__init__(front_side, back_side, message)
        self.question_a = question_a
        self.question_b = question_b
        self.question_c = question_c

        self.answer_a = answer_a
        self.answer_b = answer_b
        self.answer_c = answer_c



class Card(abc.ABC):
    def __init__(self, config):
        self.config = config

    def flip(self):
        self.config.visible_side = self.config.front_side
        #return self._is_successful()

    def display(self):
        print(self.config.message)

    def __str__(self):
        return f'Card: message: {self.config.message}'

    @abc.abstractmethod
    def _is_successful(self):
        pass


class CombatCard(Card):
    def __init__(self, config):
        super().__init__(config)

    def _fight(self):
        while True:
            roll = Dice.double_roll()
            print('You rolled', roll)
            if roll != self.config.power:
                break
        return roll > self.config.power

    def _is_successful(self):
        won = self._fight()
        if won:
            print('You have won.')
        else:
            print('You have lost.')

        return won

    def __str__(self):
        return f'Combat Card, message: {self.config.message}, power: {self.config.power}'


class LetterCard(Card):
    def _is_successful(self):
        # you always lose when you pick this card
        return False


class TaskCard(Card):
    def _is_successful(self, task_done):
        return task_done


class QuizCard(Card):
    def _is_successful(self, answer):
        return answer
