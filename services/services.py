import random

from lexicon.lexicon import LEXICON_UA


def get_bot_choice() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_UA:
        if LEXICON_UA[key] == user_answer:
            return key
    raise Exception


def get_winner(user_choice: str, bot_choise: str) -> str:
    user_choice = _normalize_user_answer(user_choice)

    rules: dict[str, str] = {'rock': 'scissors',
                             'scissors': 'paper',
                             'paper': 'rock'}

    if user_choice == bot_choise:
        return 'nobody_won'
    elif rules[user_choice] == bot_choise:
        return 'user_won'
    else:
        return 'bot_won'
