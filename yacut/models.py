import random
from datetime import datetime
from string import ascii_letters, digits

from flask import url_for

from . import db

SYMBOLS_CHOICE = list(ascii_letters + digits)


class URLMap(db.Model):
    """
    Модель для хранения оригинальных и сокращенных URL-адресов в базе данных.

    Attributes:
        id: Первичный ключ.
        original: Оригинальный URL-адрес.
        short: Сокращенный URL-адрес.
        timestamp: Дата и время создания записи.

    Methods:
        get_unique_short_id(cls): Возвращает уникальный сокращенный идентификатор.
        from_dict(self, data): Принимает словарь данных и устанавливает атрибуты объекта.
        to_dict(self): Возвращает словарь данных, представляющих объект.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(max=256), nullable=False)
    short = db.Column(db.String(max=16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data) -> None:
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])

    def to_dict(self) -> dict:
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_to_short_link',
                short=self.short,
                _external=True
            )
        )

    @classmethod
    def get_unique_short_id(cls) -> str:
        return str(''.join(random.choice(SYMBOLS_CHOICE) for _ in range(1, 7)))
