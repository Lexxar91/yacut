from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.constants import DESCRIPTION_URL, YOUR_CHOICE, MISSING_DATA


class UrlMapForm(FlaskForm):
    """
    Форма для создания сокращенных ссылок.

    Attributes:
        original_link: Поле для ввода оригинального URL-адреса.
        custom_id: Поле для ввода пользовательского сокращенного идентификатора.
        submit: Кнопка для отправки формы.
    """
    original_link = URLField(
        DESCRIPTION_URL,
        validators=[DataRequired(message=MISSING_DATA),
                    Length(1, 256)])
    custom_id = URLField(
        YOUR_CHOICE,
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
