from string import ascii_letters, digits
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
