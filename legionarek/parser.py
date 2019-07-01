import yaml
import os
from legionarek.constants import CARD_DEFINITION_PATH
from legionarek.card import CombatCard, TaskCard, LetterCard, QuizCard
from legionarek.card import CardConfig, CombatCardConfig, LetterCardConfig, TaskCardConfig, QuizCardConfig


class Parser:
    def __init__(self):
        self.card_definitions = [
            os.path.join(CARD_DEFINITION_PATH, 'combat_cards.yml'),
            os.path.join(CARD_DEFINITION_PATH, 'letter_cards.yml'),
            os.path.join(CARD_DEFINITION_PATH, 'task_cards.yml'),
            os.path.join(CARD_DEFINITION_PATH, 'quiz_cards.yml')
        ]
        self.card_config_settings = {
            'combat': {'config': CombatCardConfig, 'additions': ['power']},
            'letter': {'config': LetterCardConfig, 'additions': []},
            'task': {'config': TaskCardConfig, 'additions': ['task']},
            'quiz': {'config': QuizCardConfig, 'additions': ['question_a', 'question_b', 'question_c', 'answer_a', 'answer_b', 'answer_c']}
        }
        self.cards = []

    @staticmethod
    def _create_card(card_type, config):
        CARD_REGISTRY = {
            'combat': CombatCard,
            'letter': LetterCard,
            'quiz': QuizCard,
            'task': TaskCard
        }
        return CARD_REGISTRY[card_type](config)

    def parse(self):
        for card_definition_file in self.card_definitions:
            with open(card_definition_file) as f:
                parsed_cards = yaml.safe_load(f)
                for parsed_card in parsed_cards['cards']:
                    card_type = parsed_card['type']
                    card_config_setting = self.card_config_settings[card_type]
                    addition_config = []
                    for addition in card_config_setting['additions']:
                        addition_config.append(parsed_card[addition])
                    card_config = card_config_setting['config'](
                        parsed_card['front'],
                        parsed_card['back'],
                        parsed_card['message'],
                        *addition_config
                    )
                    self.cards.append(self._create_card(card_type, card_config))
