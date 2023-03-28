import random
from string import ascii_letters, digits

from yacut.constants import CHARS
from yacut.models import URLMap

SYMBOLS_CHOICE = list(ascii_letters + digits)


def check_symbols(custom_id):
    """
    Функция проверки символов в пользовательском идентификаторе.

    :param custom_id: Пользовательский идентификатор.
    :return: True, если все символы в пользовательском идентификаторе соответствуют допустимым символам,
             False - в противном случае.
    """
    for elem in custom_id:
        if elem not in SYMBOLS_CHOICE:
            return False
    return True


def check_short_link(custom_id):
    """
    Функция проверки наличия пользовательского идентификатора в базе данных.

    :param custom_id: Пользовательский идентификатор.
    :return: Пользовательский идентификатор, если он уже есть в базе данных, None - в противном случае.
    """
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        return custom_id
    return None


def get_unique_short_id() -> str:
    return str(''.join(random.choice(CHARS) for _ in range(1, 7)))
