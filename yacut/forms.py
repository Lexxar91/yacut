from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional

from yacut.constants import DESCRIPTION_URL, MISSING_DATA, YOUR_CHOICE


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
                    Length(max=256)])
    custom_id = URLField(
        YOUR_CHOICE,
        validators=[Length(max=16), Optional()]
    )
    submit = SubmitField('Создать')
