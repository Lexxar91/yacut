from datetime import datetime
from yacut import db
import random

from flask import url_for
from sqlalchemy_utils import URLType

from .constants import CHARS


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
    original = db.Column(URLType, nullable=False)
    short = db.Column(URLType, nullable=False, unique=True)
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
        return str(''.join(random.choice(CHARS) for _ in range(1, 7)))
