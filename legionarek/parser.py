import yaml
import os
from legionarek.constants import CARD_DEFINITION_PATH
from legionarek.card import CardConfig, CombatCard, TaskCard, LetterCard, QuizCard


class Parser:
    def __init__(self):
        self.card_definitions = {
            'combat_cards': os.path.join(CARD_DEFINITION_PATH, 'combat_cards.yml')
#            'letter_cards': os.path.join(CARD_DEFINITION_PATH, 'letter_cards.yml'),
#            'task_cards': os.path.join(CARD_DEFINITION_PATH, 'task_cards.yml'),
#            'quiz_cards': os.path.join(CARD_DEFINITION_PATH, 'quiz_cards.yml')
        }
        self.cards = []

    def create_card(self, card_type, config, power=None):
        CARD_REGISTRY = {
            'combat': CombatCard,
            'letter': LetterCard,
            'quiz': QuizCard,
            'task': TaskCard
        }

        if card_type != 'combat':
            card = CARD_REGISTRY[card_type](config)
        else:
            card = CARD_REGISTRY[card_type](config, power)
        return card

    def parse(self):
        for card_type, card_definition in self.card_definitions.items():
            with open(card_definition) as f:
                parsed_cards = yaml.safe_load(f)
                for parsed_card in parsed_cards['cards']:
                    card_type = parsed_card['type']
                    card_config = CardConfig(
                        front_side=parsed_card['front'],
                        back_side=parsed_card['back'],
                        message=parsed_card['message']
                    )
                    if card_type == 'combat':
                        self.cards.append(self.create_card(card_type, card_config, parsed_card['power']))
                    else:
                        self.cards.append(self.create_card(card_type, card_config))
