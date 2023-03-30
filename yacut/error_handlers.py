from http import HTTPStatus
from flask import jsonify, render_template

from . import db, app
from .models import URLMap


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """
    Функция обработчика ошибки 404. Отображает страницу с сообщением о том, что запрошенная страница не найдена.

    :param error: Объект ошибки.
    :return: HTML-страница с сообщением о том, что запрошенная страница не найдена.
    """
    return render_template('404.html'), HTTPStatus.NOT_FOUND


class InvalidAPIUsage(Exception):
    """
    Класс исключения для обработки ошибок в API.

    :param message: Сообщение об ошибке.
    :param status_code: Код HTTP-статуса ошибки.
    """
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """
        Функция преобразования объекта исключения в словарь.

        :return: Словарь с сообщением об ошибке.
        """
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """
    Функция обработчика ошибок в API. Возвращает сообщение об ошибке в формате JSON.

    :param error: Объект ошибки.
    :return: Сообщение об ошибке в формате JSON.
    """
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """
    Функция обработчика ошибки 500. Отображает страницу с сообщением о технической проблеме на сервере.

    :param error: Объект ошибки.
    :return: HTML-страница с сообщением о технической проблеме на сервере.
    """
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


def check_short_link(custom_id):
    """
    Функция проверки наличия пользовательского идентификатора в базе данных.

    :param custom_id: Пользовательский идентификатор.
    :return: Пользовательский идентификатор, если он уже есть в базе данных, None - в противном случае.
    """
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        return custom_id
    return None
